// Entry program for the make.fun news-image-20261126 competition.
//
// The front page is drawn offline by draw.py (PIL primitives, no network,
// no external assets) and committed here as entry.png. This program only
// checks that the file is a real PNG inside the size cap and copies it to
// the directory the harness names in MAKEFUN_OUTPUT_DIR. It writes the
// exact bytes it read, so two runs produce identical output.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const here = fileURLToPath(new URL(".", import.meta.url));
const src = join(here, "entry.png");
const bytes = readFileSync(src);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("entry.png does not start with PNG magic bytes");
  process.exit(1);
}
if (bytes.length > MAX_BYTES) {
  console.error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
writeFileSync(dest, bytes);
console.log(`wrote ${dest} (${bytes.length} bytes)`);
