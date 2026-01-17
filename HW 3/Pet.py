# Create a class called Pet with attributes name and age. 

# Implement a method within the class to calculate the age of the pet in equivalent human years. 

# Additionally, create a class variable called species to store the species of the pet. 

# Implement a method within the class that takes the species of the pet as input 
# and returns the average lifespan for that species.

#Instantiate three objects of the Pet class with different names, ages, and species.

#Calculate and print the age of each pet in human years.

#Use the average lifespan function to retrieve and print the average lifespan 
# for each pet's species.

#creating a class for pets
# 1. Create the class
class Pet:
    species = "Unknown"  # Class variable

    def __init__(self, name, age, species):
        # Instance attributes
        self.name = name
        self.age = age
        self.species = species

    # Method that "takes the species as input" and returns lifespan
    def get_average_lifespan(self, species_name):
        lifespans = {
            "dog": 13,
            "cat": 15,
            "turtle": 100,
            "human": 80
        }
        # Returns the value; defaults to 0 if not found
        return lifespans.get(species_name.lower(), 0)

    # Method to calculate age in equivalent human years
    def calculate_human_years(self):
        # We assume 80 is the standard human lifespan for the ratio
        avg_life = self.get_average_lifespan(self.species)
        
        if avg_life > 0:
            # Formula: (Pet Age / Pet Lifespan) * Human Lifespan
            human_age = (self.age / avg_life) * 80
            return round(human_age, 1)
        return "Unknown"

# 2. Instantiate three objects
pet1 = Pet("Bob", 4, "cat")
pet2 = Pet("Sam", 6, "dog")
pet3 = Pet("Greg", 34, "turtle")

# 3. Calculate and print results
pets = [pet1, pet2, pet3]

print("--- PET HOMEWORK REPORT ---")
for p in pets:
    # Retrieve the lifespan and human years using the class methods
    lifespan = p.get_average_lifespan(p.species)
    human_equiv = p.calculate_human_years()
    
    print(f"Pet Name: {p.name}")
    print(f"Species:  {p.species}")
    print(f"Average Lifespan: {lifespan} years")
    print(f"Equivalent Human Age: {human_equiv} years")
    print("-" * 25)

   # Gemini Conversation link: https://gemini.google.com/share/ddaca8045075