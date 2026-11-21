// News-image entry for 21 November 2026 (Node 22, standard library only).
// The infographic lives in this repository as entry.png; the program copies it
// byte-for-byte to /output/entry.png. No network, no randomness: two runs
// produce identical bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
