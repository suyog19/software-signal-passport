"""Bounded, non-executing report inspection. No archive extraction."""
import io
import json
import stat
import zipfile
import xml.etree.ElementTree as ET
from .schema import Invalid, parse
from .security import path_ok, redact

def summarize(raw):
    if len(raw) > 1000000:
        raise Invalid("Report archive exceeds 1 MB")
    summaries = []
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            items = archive.infolist()
            if len(items) > 50 or sum(i.file_size for i in items) > 1000000:
                raise Invalid("Report archive expansion exceeds limits")
            for item in items:
                if not path_ok(item.filename.rstrip("/")) or stat.S_ISLNK(item.external_attr >> 16):
                    raise Invalid("Unsafe report archive entry")
                if item.is_dir():
                    continue
                if item.file_size > 200000 or item.file_size > max(item.compress_size, 1)*100:
                    raise Invalid("Report compression/size exceeds limits")
                with archive.open(item) as stream:
                    body = stream.read(200001)
                if len(body) > 200000:
                    raise Invalid("Report entry exceeds limits")
                if item.filename.endswith(".xml"):
                    if b"<!DOCTYPE" in body.upper() or b"<!ENTITY" in body.upper():
                        raise Invalid("Report XML declarations are prohibited")
                    root = ET.fromstring(body)
                    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
                    if suites:
                        fields = {}
                        for name in ("tests", "failures", "errors", "skipped"):
                            values = [s.get(name) for s in suites]
                            fields[name] = sum(int(v) for v in values) if all(v is not None and v.isdigit() for v in values) else "Unknown"
                        summaries.append(item.filename+": JUnit "+json.dumps(fields, sort_keys=True))
                elif item.filename.endswith((".json", ".sarif")):
                    data = parse(body.decode())
                    if isinstance(data, dict) and isinstance(data.get("runs"), list):
                        results = [r for run in data["runs"] if isinstance(run, dict) for r in run.get("results", []) if isinstance(r, dict)]
                        summaries.append(item.filename+f": SARIF {len(results)} reported results; severity/coverage not independently verified")
                    elif isinstance(data, dict) and isinstance(data.get("total"), dict):
                        metrics = {}
                        for field in ("lines", "statements", "functions", "branches"):
                            value = data["total"].get(field, {}).get("pct")
                            metrics[field] = value if type(value) in {int, float} and 0 <= value <= 100 else "Unknown"
                        summaries.append(item.filename+": coverage percentages "+json.dumps(metrics, sort_keys=True))
        return [redact(s)[:900] for s in summaries] or ["No supported JUnit, SARIF or coverage-summary content found"]
    except (zipfile.BadZipFile, ET.ParseError, UnicodeError, ValueError, TypeError, AttributeError, KeyError):
        raise Invalid("Malformed report content; not accepted as evidence") from None
