import "server-only";
/**
 * Calcul des prix clients. Ce module lit les prix d'achat : il ne doit être importé
 * QUE par des server components / la génération statique. `server-only` fait échouer
 * le build si un composant client l'importe. Seuls les prix finaux sont envoyés au navigateur.
 */
import raw from "../../content/products.json";
import { ARRONDI_PRIX, COEF_PRIX } from "../../content/site.config";
import { computeClientPrices, type ClientProduct, type RawProduct } from "./pricing-core";

export function getProducts(): ClientProduct[] {
  return (raw as RawProduct[]).map((p) => computeClientPrices(p, COEF_PRIX, ARRONDI_PRIX));
}

export function getProduct(slug: string): ClientProduct | undefined {
  return getProducts().find((p) => p.slug === slug);
}
