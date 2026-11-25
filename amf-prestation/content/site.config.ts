/**
 * Configuration éditable du site AMF Prestation.
 * Tout ce qui est marqué « À COMPLÉTER » est listé dans `aCompleter` en bas de fichier.
 */

/** Prix client = prix d'achat × COEF_PRIX, arrondi aux 0,50 € supérieurs.
 *  1.67 ≈ 40 % de marge brute minimum. */
export const COEF_PRIX = 1.67;

/** Arrondi appliqué au prix client (0.5 = aux 50 centimes supérieurs). */
export const ARRONDI_PRIX = 0.5;

/** Afficher la référence fournisseur sur les fiches produit (déconseillé). */
export const AFFICHER_REF_FOURNISSEUR = false;

/** Quantités */
export const QUANTITE_MIN = 10;
export const SEUIL_SUR_MESURE = 100; // dès 100 pcs, on met en avant la Cuvée Sur-mesure
export const SEUIL_SUR_DEVIS = 500; // 500 pcs et + : « Sur devis » côté Atelier Paris

export const site = {
  nom: "AMF Prestation",
  signature: "by All My Friends",
  baseline: "Votre merch, dessiné à Paris. Dès 10 pièces.",
  description:
    "Studio de merchandising textile pour les maisons de champagne, domaines, agences événementielles, clubs et entreprises. T-shirts, sweats, polaires et casquettes personnalisés dès 10 pièces.",
  url: "https://amf-prestation.fr", // À COMPLÉTER : domaine définitif
  ancrage: "Paris × Champagne",

  contact: {
    email: "", // À COMPLÉTER
    telephone: "", // À COMPLÉTER
    instagram: "", // À COMPLÉTER
  },

  legal: {
    raisonSociale: "AMF Prestation", // À COMPLÉTER : forme juridique
    siret: "", // À COMPLÉTER
    adresse: "", // À COMPLÉTER
    directeurPublication: "Arthur Boulonnais",
    hebergeur: "Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, États-Unis",
    /** Si franchise en base de TVA : "TVA non applicable, art. 293 B du CGI". Sinon laisser vide. */
    mentionTVA: "", // À COMPLÉTER
  },

  mentionPrix: "Prix HT / pièce, marquage recto-verso inclus.",

  /** Délais : formulation provisoire neutre tant que les vrais délais ne sont pas renseignés. */
  delais: {
    atelierParis: null as string | null, // À COMPLÉTER, ex. "8 à 10 jours ouvrés après BAT"
    usine: null as string | null, // À COMPLÉTER, ex. "6 à 8 semaines après BAT"
    provisoireParis: "Délais courts, confirmés à la validation du BAT",
    provisoireUsine: "Délai de production confirmé avec votre devis",
  },

  conditions: [
    "Acompte de 40 % à la validation du BAT (non remboursable), solde à la livraison.",
    "Les délais courent à partir du BAT validé.",
    "Tolérance de ±3 % sur les quantités livrées (standard en sérigraphie).",
    "Tous les prix sont indiqués HT.",
  ],

  productions: {
    atelierParis: {
      nom: "Atelier Paris",
      label: "Express",
      quantites: "10 à 100 pièces (et plus)",
      pitch: "Imprimé à Paris, rapide, sur une sélection de modèles éprouvés.",
      personnalisation: "Marquage recto-verso, choix du modèle et du coloris",
      prix: "Prix affichés",
    },
    usine: {
      nom: "Cuvée Sur-mesure",
      label: "Sur-mesure",
      quantites: "Dès 100 pièces",
      pitch:
        "Produit dans notre usine partenaire : plus de qualité pour moins cher dès 100 pièces, et tout se personnalise.",
      personnalisation:
        "Qualité de coton, grammage (jusqu'à 280 g/m² et plus), coupe, coloris Pantone, étiquette de col, étiquettes tissées, finitions",
      prix: "Prix sur demande",
    },
  },

  cibles: [
    "Maisons de champagne",
    "Domaines & vendanges",
    "Agences événementielles",
    "Clubs & événements sportifs",
    "Entreprises & scale-ups",
    "Boutiques & caveaux",
  ],
} as const;

export type GammeId = "BRUT" | "RÉSERVE" | "MILLÉSIME" | "GRAND CRU" | "CUVÉE SUR-MESURE";

export const gammes: { id: GammeId; slug: string; accroche: string; description: string }[] = [
  { id: "BRUT", slug: "brut", accroche: "Les essentiels", description: "Légers et efficaces, 150 à 180 g/m²." },
  { id: "RÉSERVE", slug: "reserve", accroche: "Plus de tenue", description: "Coupes classiques et ajustées, 185 à 215 g/m²." },
  { id: "MILLÉSIME", slug: "millesime", accroche: "Heavy & streetwear", description: "Unisexe, oversize et boxy, 220 à 300 g/m²." },
  { id: "GRAND CRU", slug: "grand-cru", accroche: "Made in Portugal", description: "Finitions premium, étiquette satin, coton choisi." },
  {
    id: "CUVÉE SUR-MESURE",
    slug: "sur-mesure",
    accroche: "100 % à votre image",
    description: "Usine partenaire, dès 100 pièces. Grammage, coupe, coloris et étiquettes au choix. Prix sur demande.",
  },
];

/** Liste de tout ce qui reste à fournir ou valider. Affichée à chaque fin de phase. */
export const aCompleter: string[] = [
  "Catalogue Atelier Paris (source/catalogue-paris.pdf) : absent, nécessaire pour coloris + fit sheets + photos",
  "Logo All My Friends (source/logo/) : absent, wordmark typographique provisoire",
  "Photos du book (source/book/) : absentes, placeholders",
  "Prix d'achat palier 10–49 pièces (prixAchat10a49) pour chaque référence : affiché « Sur devis »",
  "Délai Atelier Paris (site.delais.atelierParis)",
  "Délai usine / Sur-mesure (site.delais.usine)",
  "Email de contact (site.contact.email) + CONTACT_EMAIL / RESEND_API_KEY sur Vercel",
  "Téléphone (site.contact.telephone)",
  "Instagram (site.contact.instagram)",
  "SIRET, forme juridique et adresse (site.legal)",
  "Mention TVA : « TVA non applicable, art. 293 B du CGI » si franchise (site.legal.mentionTVA)",
  "Domaine définitif (site.url)",
  "Logos clients pour le bandeau défilant",
  "GEMINI_API_KEY pour la génération des photos (phase 2)",
];
