// Entry program for the 21 November 2026 news image (Node 22, stdlib only).
// The finished infographic ships in this repo as entry.png; this program
// reads those bytes back and writes them to the output directory make.fun
// provides, so the graded run is a plain byte copy with no network use.
//
// Try it locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const target = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(target, { recursive: true });
const bytes = readFileSync(new URL("./entry.png", import.meta.url));
writeFileSync(`${target}/entry.png`, bytes);
