// Post the Meme, Win the Feed — entry program (Node 22, standard library only).
// The post itself is the entry: this program only hands POST.json to the grader,
// which reads the X post and its counts from there. Nothing else written here
// is scored, so this file stays deliberately small and deterministic.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const postFile = join(repoDir, "POST.json");

if (!existsSync(postFile)) {
  console.error(`POST.json not found in ${repoDir}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), readFileSync(postFile));
