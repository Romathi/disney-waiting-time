import sqlite3

raw_data = """
Pirate Galleon|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Star Wars Hyperspace Mountain|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Disney Cascade of Lights|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Disneyland Railroad Frontierland Depot|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Phantom Manor|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Reserved Viewing Area : Disney Cascade of Lights|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Le Carrousel de Lancelot |dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
La Tanière du Dragon|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Ratatouille : L’Aventure Totalement Toquée de Rémy​|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Disneyland Railroad Main Street Station|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Entry to World of Frozen|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Rustler Roundup Shootin' Gallery|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Raiponce Tangled Spin|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Toy Soldiers Parachute Drop|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Les Mystères du Nautilus|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Musical Moment with Rapunzel and Flynn|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Adventure Isle|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Thunder Mesa Riverboat Landing|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Indiana Jones™ and the Temple of Peril|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Disney Stars on Parade |dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Le Pays des Contes de Fées, presented by Vittel|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Reserved viewing area: Disney Stars on Parade|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Main Street Vehicles|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Big Thunder Mountain|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
TOGETHER: a Pixar Musical Adventure|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Disney Tales of Magic|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Orbitron®|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Pirates' Beach|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Star Tours: The Adventures Continue*|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Le Passage Enchanté d'Aladdin|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Mad Hatter's Tea Cups|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Frontierland Playground|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Animation Academy|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Disney Marching Band|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
A Celebration in Arendelle|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
RC Racer|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Mickey’s PhilharMagic|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
The Lion King: Rhythms of the Pride Lands|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Frozen: A Musical Invitation|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Alice's Curious Labyrinth|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Reserved viewing area: Disney Tales of Magic|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Autopia, presented by Avis|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Les Voyages de Pinocchio|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Casey Jr. – le Petit Train du Cirque|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
La Cabane des Robinson|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Les Tapis Volants - Flying Carpets Over Agrabah®|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
A Million Splashes of Colour|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Minnie’s Dream Factory|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Blanche-Neige et les Sept Nains®|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Mickey and the Magician|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Slinky® Dog Zigzag Spin|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Doctor Strange: Mystery of the Mystics!|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Frozen Ever After|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Stitch Live!|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Avengers Assemble: Flight Force|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Dumbo the Flying Elephant|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Crush's Coaster|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Cars ROAD TRIP|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Peter Pan's Flight|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Pirates of the Caribbean|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
Cars Quatre Roues Rallye|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Spider-Man W.E.B. Adventure|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
Buzz Lightyear Laser Blast|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
The Twilight Zone Tower of Terror|ca888437-ebb4-4d50-aed2-d227f7096968|Walt Disney Studio
"it's a small world"|dae968d5-630d-4719-8b06-3d107e944401|Disneyland Park
"""


conn = sqlite3.connect("disney_data.db")
cursor = conn.cursor()

conn.execute("""
ALTER TABLE wait_times ADD COLUMN is_favorite INTEGER DEFAULT 0
""")
conn.execute("""
ALTER TABLE wait_times ADD COLUMN park_id TEXT DEFAULT NULL
""")
conn.commit()

print("🚀 Début de la mise à jour forcée...")

# On itère sur chaque ligne de ta liste
for line in raw_data.strip().split("\n"):
    # On découpe par le pipe
    parts = line.split("|")
    if len(parts) == 3:
        attr_name = parts[0]
        p_id = parts[1].strip()
        p_name = parts[2].strip()

        # On met à jour TOUT l'historique pour cette attraction précise
        # On ne met pas de WHERE park_id IS NULL pour être sûr d'écraser le "Disneyland Paris" générique
        cursor.execute(
            """
            UPDATE wait_times
            SET park_id = ?, park_name = ?
            WHERE attraction_name = ?
        """,
            (p_id, p_name, attr_name),
        )

conn.commit()
conn.close()

print("✅ Terminé ! Ton historique est propre.")
