import sqlite3

if __name__ == "__main__":
    print("Running query_pets.py")

    connection = sqlite3.connect("pets.db")
    cursor = connection.cursor()

    while True:
        try:
            person_id = int(input("Enter a person's ID (or 1 to exit): "))
            if person_id == 1:
                print("Goodbye!")
                break

            # Fetch person
            cursor.execute("SELECT first_name, last_name, age FROM person WHERE id = ?;", (person_id,))
            person = cursor.fetchone()

            if person:
                print(f"{person[0]} {person[1]}, {person[2]} years old")

                # Fetch pet info
                cursor.execute("""
                    SELECT pet.name, pet.breed, pet.age, pet.dead
                    FROM pet
                    JOIN person_pet ON pet.id = person_pet.pet_id
                    WHERE person_pet.person_id = ?;
                """, (person_id,))
                pets = cursor.fetchall()

                for pet in pets:
                    status = "is" if pet[3] == 0 else "was"
                    print(f"{person[0]} {person[1]} {status} the owner of {pet[0]}, a {pet[1]}, that {status} {pet[2]} years old.")
            else:
                print("No person found with that ID.")

        except ValueError:
            print("Please enter a valid numeric ID.")

    connection.close()