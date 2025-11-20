import trafilatura
import os
import json
from datetime import datetime

def scrape_text_from_url(url):
    """
    Scrape and extract text from a given URL using Trafilatura.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The extracted text, or None if extraction fails.
    """
    try:
        # Fetch the webpage content
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            print(f"Failed to fetch content from {url}")
            return None
        
        # Extract the main text content
        text = trafilatura.extract(downloaded)
        if text is None:
            print(f"Failed to extract text from {url}")
            return None
        
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    urls = [
        # === SANTÉ PUBLIQUE FRANCE (Agence nationale de santé publique) ===
        "https://www.santepubliquefrance.fr/maladies-et-traumatismes/diabete/donnees/",
        "https://www.santepubliquefrance.fr/les-actualites/2024/le-diabete-en-france-continue-de-progresser",
        "https://www.santepubliquefrance.fr/les-actualites/2021/le-diabete-en-france-les-chiffres-2020",
        "https://www.santepubliquefrance.fr/les-actualites/2018/le-diabete-en-france-en-2016-etat-des-lieux",
        "https://www.santepubliquefrance.fr/maladies-et-traumatismes/diabete/articles/prevalence-et-incidence-du-diabete",
        "https://www.santepubliquefrance.fr/les-actualites/2022/etat-de-sante-des-personnes-diabetiques-en-france-1ers-resultats-de-l-etude-entred-3-en-metropole",
        
        # === HAUTE AUTORITÉ DE SANTÉ (HAS) ===
        "https://www.has-sante.fr/jcms/p_3191108/fr/strategie-therapeutique-du-patient-vivant-avec-un-diabete-de-type-2",
        "https://www.has-sante.fr/jcms/p_3520515/fr/diabete-de-type-2-les-therapies-non-medicamenteuses-d-abord",
        "https://www.has-sante.fr/jcms/p_3634754/fr/parcours-de-soins-du-patient-adulte-vivant-avec-un-diabete-de-type-2",
        "https://www.has-sante.fr/jcms/c_2012494/fr/prevention-et-depistage-du-diabete-de-type-2-et-des-maladies-liees-au-diabete",
        "https://www.has-sante.fr/jcms/p_3058418/fr/diabete-de-type-2",
        
        # === ASSURANCE MALADIE (Données épidémiologiques et prises en charge) ===
        "https://www.assurance-maladie.ameli.fr/etudes-et-donnees/cartographie-fiche-diabete",
        "https://www.assurance-maladie.ameli.fr/etudes-et-donnees/cartographie-prevalence-diabete",
        "https://www.assurance-maladie.ameli.fr/assure/actualites/avec-data-pathologies-l-assurance-maladie-partage-ses-donnees-sur-les-pathologies-en-france",
        
        # === MINISTÈRE DE LA SANTÉ ===
        "https://sante.gouv.fr/soins-et-maladies/maladies/article/diabete",
        
        # === ORGANISATION MONDIALE DE LA SANTÉ (OMS) ===
        "https://www.who.int/fr/news-room/fact-sheets/detail/diabetes",
        "https://iris.who.int/bitstream/handle/10665/254648/9789242565256-fre.pdf",  # Rapport mondial sur le diabète
        "https://www.who.int/fr/news/item/14-04-2021-new-who-global-compact-to-speed-up-action-to-tackle-diabetes",
        "https://www.who.int/fr/news/item/06-04-2016-world-health-day-2016-who-calls-for-global-action-to-halt-rise-in-and-improve-care-for-people-with-diabetes",
        "https://apps.who.int/iris/handle/10665/254648",
        
        # === FÉDÉRATION INTERNATIONALE DU DIABÈTE (IDF) ===
        "https://idf.org/fr/about-diabetes/diabetes-facts-figures/",
        
        # === INSERM (Institut National de la Santé et de la Recherche Médicale) ===
        "https://www.inserm.fr/dossier/diabete-type-2/",
        "https://www.inserm.fr/dossier/diabete-type-1/",
        "https://presse.inserm.fr/dossier-de-presse-diabete-de-type-1-linserm-fait-le-point-sur-les-recherches/37318/",
        "https://www.inserm.fr/actualite/diagnostiquer-traiter-et-accompagner-les-patients-atteints-de-diabete-atypique/",
        "https://presse.inserm.fr/cest-dans-lair/journee-mondiale-du-diabete-un-point-sur-les-avancees-recentes/",
        "https://presse.inserm.fr/diabete-de-type-2-une-piste-therapeutique-se-precise/33156/",
        "https://presse.inserm.fr/une-nouvelle-cible-therapeutique-contre-le-diabete-de-type-2-decouverte-grace-a-une-maladie-rare/41133/",
        
        # === FÉDÉRATION FRANÇAISE DES DIABÉTIQUES (Association de patients) ===
        "https://www.federationdesdiabetiques.org/information/diabete/chiffres-france",
        "https://www.federationdesdiabetiques.org/information/diabete/chiffres-monde",
        
        # === SOCIÉTÉ FRANCOPHONE DU DIABÈTE (SFD - Société savante) ===
        "https://www.sfdiabete.org/presse/chiffres-cles",
        "https://www.sfdiabete.org/recommandations/recommandations-has",
        
        # === NATIONS UNIES ===
        "https://www.un.org/fr/observances/diabetes-day",
        "https://www.paho.org/fr/campagnes/journee-mondiale-du-diabete-2023",
        "https://www.afro.who.int/fr/regional-director/speeches-messages/journee-mondiale-du-diabete-2024",

        # === diabete reunion ===
        "https://www.lareunion.ars.sante.fr/chiffre-cles-le-diabete-et-les-personnes-diabetiques-la-reunion",
        "https://la1ere.franceinfo.fr/reunion/grand-format-diabete-la-reunion-toujours-en-premiere-ligne-face-a-une-epidemie-silencieuse-1483652.html",
        "https://www.chu-reunion.fr/grande-enquete-diabete-prediabete-a-la-reunion/",
        "https://www.lareunion.ars.sante.fr/journee-mondiale-du-diabete-le-14-novembre-2025-des-premiers-indicateurs-encourageants-poursuivons",
        "https://www.cnis.fr/enquetes/prevalence-du-diabete-et-du-prediabete-a-la-reunion-etude-de-la-2024/e",
        "https://reunion.mutualite.fr/dossiers/association-diabete-nutrition-974/",
        "https://beh.santepubliquefrance.fr/beh/2023/20-21/2023_20-21_3.html",  # Prévalence du diabète à La Réunion, BEH Santé Publique France :contentReference[oaicite:0]{index=0}  
        "https://www.santepubliquefrance.fr/regions/antilles/documents/article/2023/prevalence-du-diabete-connu-dans-4-departements-et-regions-d-outre-mer-guadeloupe-martinique-guyane-et-la-reunion.-resultats-du-barometre-de-sa",  # Article Santé Publique France sur les DROM :contentReference[oaicite:1]{index=1}  
        "https://beh.santepubliquefrance.fr/beh/2023/20-21/2023_20-21_4.html",  # Analyse de la prise en charge, inégalités, littératie en santé :contentReference[oaicite:2]{index=2}  
        "https://beh.santepubliquefrance.fr/beh/2023/20-21/2023_20-21_1.html",  # Informations sur le diagnostic, recours aux soins :contentReference[oaicite:3]{index=3}  
        "https://www.linfo.re/la-reunion/sante/diabete-a-la-reunion-10-de-la-population-atteinte-soit-le-double-de-la-metropole",  # Article local LINFO.re sur l’épidémie à La Réunion :contentReference[oaicite:4]{index=4}  
        "https://www.linfo.re/la-reunion/societe/a-la-reunion-2-femmes-sur-10-developpent-un-diabete-pendant-leur-grossesse",  # Article sur le diabète gestationnel à La Réunion :contentReference[oaicite:5]{index=5}  
        "https://www.santemagazine.fr/actualites/actualites-sante/selon-une-etude-le-diabete-est-2-fois-plus-frequent-dans-les-drom-quen-hexagone-1040576",  # Étude de Santé Magazine sur la prévalence dans les DROM :contentReference[oaicite:6]{index=6}  
        "https://www.ars.sante.fr/system/files/2023-11/Synth%C3%A8se%20etudes%20diab%C3%A8te_13.11.2023.pdf",  # Synthèse des études diabète par l’ARS Réunion :contentReference[oaicite:7]{index=7}  
        "https://beh.santepubliquefrance.fr/beh/2022/9-10/2022_9-10_1.html",  # Historique, études antérieures (ex : étude Redia) :contentReference[oaicite:8]{index=8}  
        "https://beh.santepubliquefrance.fr/beh/2010/42_43/index.htm",  # Données plus anciennes (2000-2009) sur le diabète traité à La Réunion dans les DOM :contentReference[oaicite:9]{index=9}  
    ]

    # Métadonnées sur les sources
    sources_metadata = {
        "Santé Publique France": {
            "description": "Agence nationale de santé publique, surveillance épidémiologique du diabète",
            "type": "Données officielles françaises",
            "fiabilité": "Très élevée",
            "contenu": "Statistiques, prévalence, incidence, complications"
        },
        
        "Haute Autorité de Santé (HAS)": {
            "description": "Autorité publique indépendante, recommandations de bonnes pratiques",
            "type": "Recommandations cliniques officielles",
            "fiabilité": "Très élevée",
            "contenu": "Parcours de soins, stratégies thérapeutiques, dépistage"
        },
        
        "Assurance Maladie": {
            "description": "Données de remboursement et cartographie des pathologies",
            "type": "Données médico-administratives",
            "fiabilité": "Très élevée",
            "contenu": "Prévalence, coûts, disparités territoriales"
        },
        
        "OMS": {
            "description": "Organisation Mondiale de la Santé",
            "type": "Données internationales",
            "fiabilité": "Très élevée",
            "contenu": "Épidémiologie mondiale, recommandations internationales"
        },
        
        "INSERM": {
            "description": "Institut de recherche médicale français",
            "type": "Recherche scientifique",
            "fiabilité": "Très élevée",
            "contenu": "Recherches fondamentales et cliniques, innovations"
        },
        
        "Fédération Française des Diabétiques": {
            "description": "Association de patients reconnue d'utilité publique",
            "type": "Information patients",
            "fiabilité": "Élevée",
            "contenu": "Données vulgarisées, accompagnement des patients"
        },
        
        "Société Francophone du Diabète": {
            "description": "Société savante de professionnels de santé",
            "type": "Expertise médicale",
            "fiabilité": "Très élevée",
            "contenu": "Recommandations professionnelles, données cliniques"
        },

        "Ars Reunion": {
            "description": "Agence de Santé Reunion",
            "type": "Agence de surveillance",
            "fiabilité": "Très élevée",
            "contenu": "Recommandations professionnelles, données cliniques, statistique sur la reunion"
        },

        "Santé Publique France": {
        "description": "Agence nationale de santé publique responsable de la surveillance épidémiologique et des études de santé en France.",
        "type": "Données officielles françaises",
        "fiabilité": "Très élevée",
        "contenu": "Prévalence, incidence, mortalité, facteurs de risque, caractéristiques socio-démographiques, prise en charge."
        },

        "BEH (Bulletin Épidémiologique Hebdomadaire)": {
            "description": "Publication scientifique de Santé Publique France présentant les études épidémiologiques françaises.",
            "type": "Revue épidémiologique officielle",
            "fiabilité": "Très élevée",
            "contenu": "Analyses détaillées sur le diabète à La Réunion, tendances temporelles, comparaisons avec les DROM et la métropole."
        },

        "ARS La Réunion": {
            "description": "Agence Régionale de Santé de La Réunion, responsable de la stratégie locale de santé publique.",
            "type": "Données institutionnelles régionales",
            "fiabilité": "Très élevée",
            "contenu": "Programmes régionaux, synthèses d’études, analyses de terrain, prévention, données locales mises à jour."
        },

        "LINFO.re": {
            "description": "Média régional réunionnais relayant des informations locales vérifiées.",
            "type": "Presse locale",
            "fiabilité": "Bonne (vérification journalistique locale)",
            "contenu": "Chiffres vulgarisés, interviews d’experts, actualités concernant le diabète à La Réunion."
        },

        "Santé Magazine": {
            "description": "Magazine national spécialisé en santé et vulgarisation médicale.",
            "type": "Média grand public",
            "fiabilité": "Moyenne à bonne",
            "contenu": "Synthèses d’études, vulgarisation, articles accessibles destinés au grand public."
        }
    }
    for url in urls:
        scraped_text = scrape_text_from_url(url)
        if scraped_text:
            print("Extracted text:")
            print(scraped_text)
            # Load existing data or create new list
            filename = 'scraped_data.json'
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)
            else:
                data_list = []
            
            # Append new data
            new_data = {
                "url": url,
                "content": scraped_text,
                "timestamp": datetime.now().isoformat()
            }
            data_list.append(new_data)
            
            # Save back
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"Data appended to {filename}")
        else:
            print(f"No text extracted for {url}.")
