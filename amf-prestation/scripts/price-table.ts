/**
 * Affiche le tableau des prix clients (checkpoint / contrôle après changement de COEF_PRIX).
 *   npx tsx scripts/price-table.ts            → tableau Markdown
 *   npx tsx scripts/price-table.ts --achat    → ajoute les prix d'achat et la marge (usage interne)
 */
import raw from "../content/products.json";
import { ARRONDI_PRIX, COEF_PRIX } from "../content/site.config";
import { computeClientPrices, PALIERS, type RawProduct } from "../src/lib/pricing-core";

const showAchat = process.argv.includes("--achat");
const eur = (v: number | null) => (v == null ? "Sur devis" : `${v.toFixed(2).replace(".", ",")} €`);

const head = ["Nom public", "Gamme", "Coupe", "Grammage", ...PALIERS.map((p) => p.label)];
if (showAchat) head.push("Achat 50/100/250", "Marge 50");
console.log(`COEF_PRIX = ${COEF_PRIX}, arrondi ${ARRONDI_PRIX} €\n`);
console.log(`| ${head.join(" | ")} |`);
console.log(`|${head.map(() => "---").join("|")}|`);
for (const p of raw as RawProduct[]) {
  const c = computeClientPrices(p, COEF_PRIX, ARRONDI_PRIX);
  const row = [c.nom, c.gamme, c.coupe, c.grammage, ...PALIERS.map((pa) => eur(c.prix[pa.id]))];
  if (showAchat) {
    const a = p.prixAchat;
    row.push(`${a["50"]} / ${a["100"]} / ${a["250"]}`);
    row.push(`${Math.round((1 - (a["50"] ?? 0) / (c.prix["50"] ?? 1)) * 100)} %`);
  }
  console.log(`| ${row.join(" | ")} |`);
}
