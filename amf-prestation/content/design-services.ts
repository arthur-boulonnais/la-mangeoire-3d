/** Offre création « Votre design ou le nôtre ». Prix HT, modifiables. */

export const designServices = {
  votreDesign: {
    titre: "Vous avez votre design",
    accroche: "On vérifie et on prépare vos fichiers pour l'impression.",
    prestations: [
      { nom: "Vectorisation logo simple", prix: 50 },
      { nom: "Logo complexe à redessiner", prixMin: 90, prixMax: 120 },
    ],
  },
  notreDesign: {
    titre: "On crée pour vous",
    accroche: "Un designer streetwear dessine votre pièce, de l'idée au fichier prêt à imprimer.",
    forfaits: [
      { id: "creation-3", nom: "Création personnalisée — 3 propositions", prix: 220, inclus: "2 allers-retours inclus sur la piste retenue" },
      { id: "creation-6", nom: "Création personnalisée — 6 propositions", prix: 380, inclus: "2 allers-retours inclus sur la piste retenue" },
    ],
    options: [
      { nom: "Proposition supplémentaire", prix: 70 },
      { nom: "Retouche hors forfait", prix: 40 },
      { nom: "Cession des fichiers sources", prix: 150 },
    ],
  },
  avantageVolume: {
    seuil: 100,
    remise: 0.5,
    texte: "Frais de création remboursés à 50 % pour toute commande de plus de 100 pièces.",
  },
  signature: {
    titre: "Signature « by All My Friends »",
    texte:
      "Acceptez une petite signature « by All My Friends » (par exemple au dos du col) et la vectorisation de votre logo vous est offerte.",
  },
} as const;

/** Forfait utilisé par défaut dans le simulateur quand « notre design » est choisi. */
export const FORFAIT_SIMULATEUR = "creation-3";
