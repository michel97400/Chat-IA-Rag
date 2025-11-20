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
