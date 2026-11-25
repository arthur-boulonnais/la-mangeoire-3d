/** Logique pure (sans import de données) : partagée entre le site et les scripts. */

export type Palier = "10" | "50" | "100" | "250" | "500";
export const PALIERS: { id: Palier; label: string; min: number }[] = [
  { id: "10", label: "10–49", min: 10 },
  { id: "50", label: "50–99", min: 50 },
  { id: "100", label: "100–249", min: 100 },
  { id: "250", label: "250–499", min: 250 },
  { id: "500", label: "500+", min: 500 },
];

export type Coloris = { nom?: string; hex: string };

export type RawProduct = {
  slug: string;
  nom: string;
  gamme: string;
  coupe: string;
  refFournisseur: string;
  page: number;
  grammage: string;
  grammageValeur: number;
  composition: string;
  tailles: string;
  details: string[];
  prixAchat10a49: number | null;
  prixAchat: Record<"50" | "100" | "250" | "500", number | null>;
  coloris: Coloris[];
  fit: string;
};

/** Ce qui part au navigateur : aucun prix d'achat, aucune référence fournisseur. */
export type ClientProduct = Omit<RawProduct, "prixAchat10a49" | "prixAchat" | "refFournisseur" | "fit" | "page"> & {
  /** Prix client HT / pièce par palier ; null = « Sur devis ». */
  prix: Record<Palier, number | null>;
  /** Plus petit prix affiché (pour tri / « à partir de »). */
  prixMin: number | null;
};

export function prixClient(achat: number | null, coef: number, arrondi: number): number | null {
  if (achat == null) return null;
  // epsilon pour éviter qu'un 17.0000001 flottant ne saute au palier suivant
  return Math.ceil((achat * coef - 1e-9) / arrondi) * arrondi;
}

export function computeClientPrices(p: RawProduct, coef: number, arrondi: number): ClientProduct {
  const prix: Record<Palier, number | null> = {
    "10": prixClient(p.prixAchat10a49, coef, arrondi),
    "50": prixClient(p.prixAchat["50"], coef, arrondi),
    "100": prixClient(p.prixAchat["100"], coef, arrondi),
    "250": prixClient(p.prixAchat["250"], coef, arrondi),
    "500": null, // 500 pcs et + : toujours « Sur devis »
  };
  const vals = Object.values(prix).filter((v): v is number => v != null);
  /* eslint-disable @typescript-eslint/no-unused-vars */
  const { prixAchat10a49, prixAchat, refFournisseur, fit, page, ...pub } = p;
  return { ...pub, prix, prixMin: vals.length ? Math.min(...vals) : null };
}

export function palierPour(quantite: number): Palier {
  let current: Palier = "10";
  for (const pa of PALIERS) if (quantite >= pa.min) current = pa.id;
  return current;
}
