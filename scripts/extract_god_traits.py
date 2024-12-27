import os
import re
import argparse

# Parentage mapping for characters

extra_fields={}
parentage={}

parentage["Greek_gods"] = {
    # Primordial Deities
    "gaia": {"mother": "chaos", "father": "none"},  # Gaia is the primordial goddess of the Earth.
    "uranus": {"mother": "gaia", "father": "none"},  # Uranus is the primordial god of the sky.
    "nyx": {"mother": "chaos", "father": "none"},  # Nyx is the primordial goddess of the night.
    "erebus": {"mother": "chaos", "father": "none"},  # Erebus is the primordial god of darkness.

    # Titans
    "cronus": {"mother": "gaia", "father": "uranus"},  # Cronus is the Titan god of time and ruler of the first generation of Titans.
    "rhea": {"mother": "gaia", "father": "uranus"},  # Rhea is the Titan goddess of fertility and motherhood.
    "oceanus": {"mother": "gaia", "father": "uranus"},  # Oceanus is the Titan god of the ocean.
    "tethys": {"mother": "gaia", "father": "uranus"},  # Tethys is the Titan goddess of fresh water.
    "hyperion": {"mother": "gaia", "father": "uranus"},  # Hyperion is the Titan god of light and the sun.
    "theia": {"mother": "gaia", "father": "uranus"},  # Theia is the Titan goddess of sight and the shining light of the clear blue sky.
    "iapetus": {"mother": "gaia", "father": "uranus"},  # Iapetus is the Titan god of mortal life.
    "crius": {"mother": "gaia", "father": "uranus"},  # Crius is the Titan god of the constellations.
    "mnemosyne": {"mother": "gaia", "father": "uranus"},  # Mnemosyne is the Titan goddess of memory.
    "themis": {"mother": "gaia", "father": "uranus"},  # Themis is the Titan goddess of divine law and order.
    "atlas": {"mother": "asia", "father": "iapetus"},  # Atlas is the Titan god who holds up the sky.
    "prometheus": {"mother": "clymene", "father": "iapetus"},  # Prometheus is the Titan god of foresight and creator of humanity.
    "epimetheus": {"mother": "clymene", "father": "iapetus"},  # Epimetheus is the Titan god of afterthought.
    "eurybia": {"mother": "gaia", "father": "uranus"},  # Eurybia is the Titan goddess of mastery over the seas.
    "asia": {"mother": "tethys", "father": "oceanus"},  # Asia is the Titan goddess of the East.

    # Olympian Gods
    "zeus": {"mother": "rhea", "father": "cronus"},  # Zeus is the king of the gods, god of the sky, thunder, and lightning.
    "hera": {"mother": "rhea", "father": "cronus"},  # Hera is the queen of the gods, goddess of marriage and family.
    "poseidon": {"mother": "rhea", "father": "cronus"},  # Poseidon is the god of the sea, earthquakes, and horses.
    "hades": {"mother": "rhea", "father": "cronus"},  # Hades is the god of the underworld and the dead.
    "demeter": {"mother": "rhea", "father": "cronus"},  # Demeter is the goddess of the harvest, fertility, and agriculture.
    "hestia": {"mother": "rhea", "father": "cronus"},  # Hestia is the goddess of the hearth, home, and family.

    # Other Deities
    "aphrodite": {"mother": "dione", "father": "zeus"},  # Aphrodite is the goddess of love, beauty, and desire.
    "apollo": {"mother": "leto", "father": "zeus"},  # Apollo is the god of the sun, music, and prophecy.
    "artemis": {"mother": "leto", "father": "zeus"},  # Artemis is the goddess of the moon, hunting, and wild animals.
    "ares": {"mother": "hera", "father": "zeus"},  # Ares is the god of war, violence, and bloodshed.
    "athena": {"mother": "metis", "father": "zeus"},  # Athena is the goddess of wisdom, war, and strategy.
    "hermes": {"mother": "maia", "father": "zeus"},  # Hermes is the god of travelers, commerce, and thieves.
    "hephaestus": {"mother": "hera", "father": "zeus"},  # Hephaestus is the god of fire, blacksmiths, and artisans.
    "dionysus": {"mother": "semele", "father": "zeus"},  # Dionysus is the god of wine, revelry, and ecstasy.
    "persephone": {"mother": "demeter", "father": "zeus"},  # Persephone is the goddess of the underworld and spring.
    "amphitrite": {"mother": "tethys", "father": "oceanus"},  # Amphitrite is the goddess of the sea and wife of Poseidon.
    "moirai": {"mother": "themis", "father": "zeus"},  # The Moirai are the Fates, goddesses who control human destiny.
    "nemesis": {"mother": "nyx", "father": "erebus"},  # Nemesis is the goddess of revenge and retribution.

    # Other Figures
    "helios": {"mother": "theia", "father": "hyperion"},  # Helios is the god of the sun.
    "selene": {"mother": "theia", "father": "hyperion"},  # Selene is the goddess of the moon.
    "eos": {"mother": "theia", "father": "hyperion"},  # Eos is the goddess of the dawn.
    "styx": {"mother": "tethys", "father": "oceanus"},  # Styx is the goddess of the river Styx, which separates the living from the dead.
    "pallas": {"mother": "eurybia", "father": "crius"},  # Pallas is the god of war and wisdom.
    "nike": {"mother": "styx", "father": "pallas"},  # Nike is the goddess of victory.
    "eros": {"mother": "aphrodite", "father": "ares"},  # Eros is the god of love and desire.
    "tyche": {"mother": "aphrodite", "father": "zeus"}  # Tyche is the goddess of fortune and luck.
}
extra_fields["Greek_gods"] = (
                f"\n\tdynasty=greek_gods_dynasty"
                f"\n\tdynasty_house=greek_gods_dynasty"
                f"\n\tculture=\"greek\""
                f"\n\treligion=\"hellenic_pagan\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            )

parentage["Egypt_gods"] = {
    # Primordial Deities
    "nun": {"mother": "chaos", "father": "none"},  # Nun is the primordial waters from which all creation emerged.

    # Creator and Supreme Deities
    "amun-ra": {"mother": "nun", "father": "none"},  # Amun-Ra is the sun god and creator of the world.
    "neith": {"mother": "nun", "father": "none"},  # Neith is the goddess of war, weaving, and wisdom.
    "menhit": {"mother": "nun", "father": "none"},  # Menhit is a lioness goddess associated with war.

    # Sky and Earth Deities
    "geb": {"mother": "tefnut", "father": "shu"},  # Geb is the earth god, associated with the fertile land.
    "nut": {"mother": "tefnut", "father": "shu"},  # Nut is the sky goddess, often depicted arching over the earth.
    "shu": {"mother": "menhit", "father": "amun-ra"},  # Shu is the god of air and the space between heaven and earth.
    "tefnut": {"mother": "menhit", "father": "amun-ra"},  # Tefnut is the goddess of moisture, rain, and fertility.

    # Osirian Family (Gods of Life, Death, and Rebirth)
    "osiris": {"mother": "nut", "father": "geb"},  # Osiris is the god of life, death, and resurrection.
    "isis": {"mother": "nut", "father": "geb"},  # Isis is the goddess of magic, motherhood, and fertility.
    "set": {"mother": "nut", "father": "geb"},  # Set is the god of chaos, desert, and storms.
    "nephthys": {"mother": "nut", "father": "geb"},  # Nephthys is the goddess of night, mourning, and funerary rites.
    "horus": {"mother": "isis", "father": "osiris"},  # Horus is the god of the sky and kingship, often depicted as a falcon.
    "anubis": {"mother": "nephthys", "father": "set"},  # Anubis is the god of mummification and the afterlife.

    # War and Protection Deities
    "anhur": {"mother": "menhit", "father": "amun-ra"},  # Anhur is a god of war, hunting, and protection.
    "serket": {"mother": "neith", "father": "set"},  # Serket is the goddess of scorpions and protection.
    "sekhmet": {"mother": "menhit", "father": "amun-ra"},  # Sekhmet is the lioness goddess of war, healing, and destruction.
    "bastet": {"mother": "isis", "father": "amun-ra"},  # Bastet is the goddess of home, fertility, and childbirth, often depicted as a cat.

    # Wisdom and Knowledge Deities
    "thoth": {"mother": "nun", "father": "none"},  # Thoth is the god of wisdom, writing, and the moon.

    # Fertility, Justice, and Order
    "maat": {"mother": "hathor", "father": "amun-ra"},  # Maat is the goddess of truth, justice, and cosmic order.
    "hathor": {"mother": "menhit", "father": "amun-ra"},  # Hathor is the goddess of love, joy, and music, often depicted as a cow or with cow horns.

    # Theban Triad (Gods of Thebes)
    "mut": {"mother": "none", "father": "amun-ra"},  # Mut is the mother goddess and consort of Amun.
    "khonsu": {"mother": "mut", "father": "amun-ra"},  # Khonsu is the god of the moon and time.

    # Other Deities
    "sobek": {"mother": "neith", "father": "set"}  # Sobek is the crocodile god, associated with water, fertility, and protection.
}
extra_fields["Egypt_gods"] = (
                f"\n\tdynasty=egypt_gods_dynasty"
                f"\n\tdynasty_house=egypt_gods_dynasty"
                f"\n\tculture=\"egyptian\""
                f"\n\treligion=\"kushitism_pagan\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            ) 

parentage["Norse_gods"] = {
    # Aesir Gods (Main Deities of the Norse Pantheon)
    "baldr": {"mother": "frigga", "father": "odin"},  # Son of Odin and Frigga
    "freyja": {"mother": "unknown", "father": "njord"},  # Goddess of love, beauty, and fertility
    "freyr": {"mother": "unknown", "father": "njord"},  # God of fertility, prosperity, and peace
    "heimdall": {"mother": "unknown", "father": "odin"},  # Guardian of the Bifrost, son of Odin
    "hod": {"mother": "frigga", "father": "odin"},  # God associated with winter and darkness
    "hel": {"mother": "angrboda", "father": "loki"},  # Goddess of the underworld, daughter of Angrboda and Loki
    "fenrir": {"mother": "angrboda", "father": "loki"},  # Giant wolf, son of Loki and Angrboda
    "jormungandr": {"mother": "angrboda", "father": "loki"},  # The Midgard Serpent, child of Loki and Angrboda
    "loki": {"mother": "laufey", "father": "farbauti"},  # Trickster god, father of Hel, Fenrir, and Jormungandr
    "njord": {"mother": "unknown", "father": "unknown"},  # God of the sea, wind, and wealth
    "odin": {"mother": "bestla", "father": "bor"},  # Allfather of the Aesir, god of wisdom, war, and death
    "thor": {"mother": "jord", "father": "odin"},  # God of thunder, son of Odin and Jord
    "tyr": {"mother": "unknown", "father": "odin"},  # God of war and justice
    "vidar": {"mother": "grid", "father": "odin"},  # Son of Odin, god of vengeance
    "vali": {"mother": "rindr", "father": "odin"},  # God of vengeance, son of Odin and Rindr
    "frigga": {"mother": "none", "father": "ymir"},  #
    "ullr": {"mother": "sif", "father": "thor"},  #
    "thrud": {"mother": "sif", "father": "thor"},  #

    # Jotnar (Giants)
    "skadi": {"mother": "unknown", "father": "thjazi"},  # Goddess of winter and hunting, daughter of the giant Thjazi
    "thjazi": {"mother": "unknown", "father": "ymir"},  
    "sif": {"mother": "unknown", "father": "ymir"},  # Wife of Thor, associated with fertility and harvest
    "idunn": {"mother": "jord", "father": "odin"},  # Goddess of youth, keeper of the golden apples
    "bragi": {"mother": "jord", "father": "odin"},  # God of poetry, son of Odin
    "aegir": {"mother": "unknown", "father": "fornjot"},  # God of the sea, associated with storms and the ocean
    "ran": {"mother": "unknown", "father": "odin"},  # Goddess of the sea, wife of Aegir
    "forseti": {"mother": "unknown", "father": "baldr"},  # God of justice and reconciliation, son of Baldr

    # Primordial Giants and Deities
    "ymir": {"mother": "chaos", "father": "none"},  # The first being, the ancestor of all giants, born from the chaos
    "buri": {"mother": "none", "father": "ymir"},  # The first god, ancestor of the Aesir, father of Bor
    "bor": {"mother": "none", "father": "buri"},  # Father of Odin, Vili, and Ve, son of Buri
    "sol": {"mother": "none", "father": "ymir"},  # 
    "bestla": {"mother": "unknown", "father": "ymir"},  # Mother of Odin, Vili, and Ve
    "farbauti": {"mother": "unknown", "father": "ymir"},  # Father of Loki, husband of Laufey
    "laufey": {"mother": "unknown", "father": "ymir"},  # Mother of Loki, wife of Fárbauti

    # Other Deities and Beings
    "jord": {"mother": "none", "father": "ymir"},  # Earth goddess, mother of Thor
    "angrboda": {"mother": "none", "father": "ymir"},  # Mother of Hel, Fenrir, and Jormungandr, consort of Loki
    "fornjot": {"mother": "none", "father": "ymir"}  #
}
extra_fields["Norse_gods"] = (
                f"\n\tdynasty=norse_gods_dynasty"
                f"\n\tdynasty_house=norse_gods_dynasty"
                f"\n\tculture=\"norse\""
                f"\n\treligion=\"norse_pagan\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            ) 


parentage["Judaism_gods"] = {
    # God (Supreme Creator)
    "elohim": {"mother": "chaos", "father": "none"},  # God is the creator of everything.

    # Archangels
    "michael": {"mother": "elohim", "father": "god"},  # Archangel of protection, leader of the heavenly armies.
    "gabriel": {"mother": "elohim", "father": "god"},  # Archangel of communication, God's primary messenger.
    "raphael": {"mother": "elohim", "father": "god"},  # Archangel of healing, guide of the faithful.
    "uriel": {"mother": "elohim", "father": "god"},  # Archangel of wisdom and enlightenment.

    # Angels of the Divine Presence
    "metatron": {"mother": "elohim", "father": "god"},  # Once Enoch, transformed into Metatron, a scribe of heaven.
    "sandalphon": {"mother": "elohim", "father": "god"},  # Once Elijah, transformed into Sandalphon, angel of prayers.

    # Fallen Angels
    "lucifer": {"mother": "elohim", "father": "god"},  # Once a high-ranking angel, rebelled against God and became Satan.
    "azazel": {"mother": "elohim", "father": "god"},  # Associated with sin and corruption, often linked to the scapegoat ritual.
    "lilith": {"mother": "elohim", "father": "god"},  # In apocryphal texts, created as Adam's first wife, later cast out.

    # Key Human Figures
    "adam": {"mother": "elohim", "father": "god"},  # First human created by God.
    "eve": {"mother": "elohim", "father": "god"},  # Created from Adam's rib as his companion.

    # Other Key Angels
    "raziel": {"mother": "elohim", "father": "god"},  # Angel of mysteries and divine secrets.
    "zadkiel": {"mother": "elohim", "father": "god"},  # Angel of mercy and forgiveness.
    "jophiel": {"mother": "elohim", "father": "god"},  # Angel of beauty and wisdom.
    "chamuel": {"mother": "elohim", "father": "god"},  # Angel of love and harmony.
    "ariel": {"mother": "elohim", "father": "god"},  # Angel associated with nature and animals.
    "haniel": {"mother": "elohim", "father": "god"},  # Angel of joy and divine grace.
}
extra_fields["Judaism_gods"] = (
                f"\n\tdynasty=judaism_gods_dynasty"
                f"\n\tdynasty_house=judaism_gods_dynasty"
                f"\n\tculture=\"ashkenazi\""
                f"\n\treligion=\"rabbinism\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            ) 



parentage["Hindu_gods"] = {
    # Primordial Deities
    "brahman": {"mother": "chaos", "father": "none"},  # Brahman is the ultimate reality and cosmic principle.

    # Creator, Preserver, and Destroyer (Trimurti)
    "brahma": {"mother": "none", "father": "brahman"},  # Brahma is the creator god, part of the Trimurti.
    "vishnu": {"mother": "none", "father": "brahman"},  # Vishnu is the preserver god, part of the Trimurti.
    "shiva": {"mother": "none", "father": "brahman"},  # Shiva is the destroyer and transformer, part of the Trimurti.

    # Consorts of the Trimurti
    "saraswati": {"mother": "none", "father": "brahman"},  # Saraswati is the goddess of knowledge, music, and wisdom, consort of Brahma.
    "lakshmi": {"mother": "none", "father": "brahman"},  # Lakshmi is the goddess of wealth and prosperity, consort of Vishnu.
    "parvati": {"mother": "none", "father": "brahman"},  # Parvati is the goddess of love, fertility, and devotion, consort of Shiva.
    "aditi": {"mother": "none", "father": "brahman"},  # 
    "kashyapa": {"mother": "none", "father": "brahman"},  # 


    # Children of the Trimurti
    "ganesha": {"mother": "parvati", "father": "shiva"},  # Ganesha is the god of wisdom, remover of obstacles.
    "kartikeya": {"mother": "parvati", "father": "shiva"},  # Kartikeya is the god of war and victory.

    # Celestial Deities
    "indra": {"mother": "aditi", "father": "kashyapa"},  # Indra is the king of gods and ruler of the heavens.
    "agni": {"mother": "none", "father": "brahman"},  # Agni is the god of fire and sacrifices.
    "surya": {"mother": "aditi", "father": "kashyapa"},  # Surya is the sun god and source of light.
    "chandra": {"mother": "none", "father": "brahman"},  # Chandra is the moon god and associated with the mind.

    # Other Deities
    "hanuman": {"mother": "anjani", "father": "kesari"},  # Hanuman is a devotee of Rama and symbol of strength and devotion.
    "yamraj": {"mother": "saranyu", "father": "surya"},  # Yama is the god of death and dharma.
    "varuna": {"mother": "aditi", "father": "kashyapa"},  # Varuna is the god of water and cosmic order.
    "vayu": {"mother": "aditi", "father": "kashyapa"},  # Vayu is the god of wind and air.
    "saranyu": {"mother": "anjani", "father": "brahman"},  #

    # Consorts and Children of Celestial Deities
    "shachi": {"mother": "none", "father": "none"},  # Shachi (Indrani) is the consort of Indra, goddess of beauty and power.
    "savarna": {"mother": "saranyu", "father": "surya"},  # Savarna is the daughter of Surya (the sun god).
    "ashvins": {"mother": "saranyu", "father": "surya"},  # The Ashvins, twin gods of health, are children of Surya and Saranyu.
    "manu": {"mother": "saranyu", "father": "surya"},  # Manu is the progenitor of humanity.

    # Demons and Anti-Gods
    "hiranyakashipu": {"mother": "danu", "father": "kashyapa"},  # Hiranyakashipu is a demon king and enemy of Vishnu.
    "ravana": {"mother": "none", "father": "brahman"},  # Ravana is the demon king of Lanka, antagonist of the Ramayana.
    "meghnad": {"mother": "mandodari", "father": "ravana"},  # Meghnad (Indrajit) is the son of Ravana and Mandodari.

    # Goddess Shakti and Her Forms
    "durga": {"mother": "none", "father": "brahman"},  # Durga is a warrior goddess, the protector of dharma.
    "kali": {"mother": "none", "father": "brahman"},  # Kali is the fierce form of Parvati, representing destruction and time.
}
extra_fields["Hindu_gods"] = (
                f"\n\tdynasty=hindu_gods_dynasty"
                f"\n\tdynasty_house=hindu_gods_dynasty"
                f"\n\tculture=\"hindustani\""
                f"\n\treligion=\"vajrayana\""
                f"\n\t847.1.1="+"{"+" birth = \"847.1.1\" }"
            ) 



def delete_files_except_gitkeep(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip if the file is .gitkeep
        if filename == ".gitkeep":
            continue
        
        # Check if it's a file and delete it
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        # Optionally, handle directories (e.g., delete or skip)
        elif os.path.isdir(file_path):
            print(f"Skipped directory: {file_path}")


# Function to extract block content by key
def extract_info(key, content):
    start_index = content.find(f"{key}={{")
    if start_index == -1:
        return None

    brace_count = 0
    end_index = start_index + len(key) + 1
    while end_index < len(content):
        if content[end_index] == '{':
            brace_count += 1
        elif content[end_index] == '}':
            brace_count -= 1
        if brace_count == 0:
            break
        end_index += 1

    return content[start_index + len(key) + 1:end_index] if brace_count == 0 else None

# Method to replace multiple tabs with a single tab
def replace_multiple_tabs_with_one(content):
   # Step 1: Replace spaces with tabs
    content = content.replace(' ', '\t')
    # Step 2: Replace multiple consecutive tabs with a single tab
    cleaned_content = re.sub(r'\t+', '\t', content)
    return cleaned_content

# Function to process skills and traits in the content
def process_skills(match):
    skills = list(map(int, match.group(1).split()))
    skill_names = ["diplomacy", "martial", "stewardship", "intrigue", "learning", "prowess"]
    return "\n	".join(f"{name}={value}" for name, value in zip(skill_names, skills))

def process_traits(match):
    traits = match.group(1).split()
    return "\n	".join(f"trait={trait}" for trait in sorted(traits))

# Function to clean unwanted content
def clean_content(content):
    # Define regex patterns to clean
    patterns = [
        r'culture=[^\n]*',  # remove override block
        r'faith=[^\n]*',  # remove override block
    ]
    # Apply all regex patterns to clean the content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content

# Function to add additional fields to blocks (e.g., DNA, culture, faith)
def add_stuff_blocks(content, stuff):
    block_pattern = r"(\w+)\s*=\s*\{([\s\S]*?)}"
    def add_stuff_field(match):
        block_name = match.group(1)
        block_content = match.group(2).strip()
        return f"{block_name} = {{\n	{stuff}={block_name}\n      {block_content}\n}}"
    return re.sub(block_pattern, add_stuff_field, content)

# Function to process a file, extracting skills, traits, and adding parentage fields
def process_file(input_file, output_file, parentage=None, add_fields=None,extra_fields=None):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(r"skill=\{([\s\d]+)\}", process_skills, content)
    content = re.sub(r"traits=\{([^\}]+)\}", process_traits, content)

    if add_fields:
        content = add_stuff_blocks(content, add_fields)

    if parentage:
        character_name = os.path.splitext(os.path.basename(input_file))[0]
        if character_name in parentage:
            new_fields = (
                f"\n\tmother={parentage[character_name]['mother']}"
                f"\n\tfather={parentage[character_name]['father']}"
            )
            new_fields+=extra_fields
            if not re.search(r"^\s*mother=", content, re.MULTILINE):
                content = re.sub(r"(\{)", rf"\1{new_fields}", content, count=1)


    content=replace_multiple_tabs_with_one(content)
    
    with open(output_file, 'w+', encoding='utf-8') as file:
        file.write(content)

# Function to combine multiple files into one
def combine_files(input_folder, output_folder, output_filename):
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, output_filename)

    with open(output_file_path, 'w+', encoding='utf-8') as output_file:
        for filename in sorted(os.listdir(input_folder)):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    output_file.write(input_file.read())

    print(f"All files combined into: {output_file_path}")

# Main Processing Logic
def main():
    # Folder paths
    source_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\Rulers")
    target_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\mod\\Pantheons\\build\\characters")
    final_folder = os.path.expanduser("~\\DOCUMENTS\\PARADOX INTERACTIVE\\CRUSADER KINGS III\\mod\\Pantheons\\history\\characters")

    # Argument parser to take folder path as input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder_path", 
        type=str, 
        help="The path to the folder where where the gods files are"
    )
    # Parse the arguments
    args = parser.parse_args()

    if not args.folder_path:
        exit(0)

    source_folder += "\\"+args.folder_path
    target_folder += "\\"+args.folder_path

    #clean build folder
    delete_files_except_gitkeep(target_folder)

    # Iterate through source files and process them
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        if os.path.isfile(source_file_path):
            with open(source_file_path, 'r', encoding='utf-8') as file:
                source_content = file.read()

            data = extract_info("config", source_content)
            dataover = extract_info("portrait_override", source_content)
            if data:
                lowercase_filename = os.path.splitext(filename)[0].lower()
                content = f"\n{lowercase_filename} = {data} portrait_override={dataover}\n}}"+"}"+"\n\n"

                with open(os.path.join(target_folder, lowercase_filename), 'w+', encoding='utf-8') as file:
                    file.write(content)

    # Clean target files and add parentage & dynasty
    for filename in os.listdir(target_folder):
        target_file_path = os.path.join(target_folder, filename)
        if os.path.isfile(target_file_path):
            with open(target_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            cleaned_content = clean_content(content)

            with open(target_file_path, 'w+', encoding='utf-8') as cleaned_file:
                cleaned_file.write(cleaned_content)

            process_file(target_file_path, target_file_path, parentage[str(args.folder_path)], "dna", extra_fields[str(args.folder_path)])

    # Combine files into the final output file
    combine_files(target_folder, final_folder, f"characters_{args.folder_path}.txt")

# Run the main function
if __name__ == "__main__":
    main()
