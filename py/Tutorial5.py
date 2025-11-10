# Using else and finally with try statements
try:
    file=open('data.txt', 'r')
except FileNotFoundError:
    print("File not found! Please check the file path.")
else:
    content = file.read()
    print(f"File read successfully! Content:\n{content}")
finally:
    if 'file' in locals() and not file.closed:
        file.close()
    print("Cleanup completed.")

print("")
# Basic Class Definition

print("Game Character Exercise")
print("-" * 20)

class GameCharacter:
    def __init__(self, name, health=100, attack_power=10):
        self.name = name
        self.health = health
        self.max_health = health  # Store max health to limit healing
        self.attack_power = attack_power
    
    def attack(self, target):
        """Attack another character"""
        target.health -= self.attack_power
        print(f"{self.name} attacks {target.name} for {self.attack_power} damage!")
        print(f"{target.name}'s health: {target.health}")
    
    def heal(self, amount=20):
        """Heal the character"""
        if self.health + amount > self.max_health:
            heal_amount = self.max_health - self.health
            self.health = self.max_health
        else:
            heal_amount = amount
            self.health += amount
            
        print(f"{self.name} heals for {heal_amount} HP!")
        print(f"Current health: {self.health}")
    
    def is_alive(self):
        """Check if character is still alive"""
        return self.health > 0

# Example usage:
# Create two characters
hero = GameCharacter("BOBOBOI", health=100, attack_power=15)
monster = GameCharacter("Makhluk Halus", health=80, attack_power=12)

# Demonstrate the game mechanics
print(f"{hero.name} starts with {hero.health} health")
print(f"{monster.name} starts with {monster.health} health")
print()

# Combat simulation
hero.attack(monster)    # Hero attacks monster
monster.attack(hero)    # Monster attacks back
print()

hero.heal()            # Hero heals
print()

hero.attack(monster)   # Hero attacks again
print()

# Check if characters are alive
print(f"{hero.name} is alive? {hero.is_alive()}")
print(f"{monster.name} is alive? {monster.is_alive()}")

print("\nHealthcare Management System")
print("-" * 30)

class Doctor:
    def __init__(self, name, specialty, is_on_call=False):
        self.name = name
        self.specialty = specialty
        self.is_on_call = is_on_call
        self.patients = []
        self.on_call_hours = 0
    
    def start_on_call(self):
        self.is_on_call = True
        print(f"Dr. {self.name} is now on call")
    
    def end_on_call(self, hours):
        self.is_on_call = False
        self.on_call_hours += hours
        print(f"Dr. {self.name} finished {hours} hours on call")
    
    def assign_patient(self, patient):
        self.patients.append(patient)
        print(f"Patient {patient.name} assigned to Dr. {self.name}")
    
    def check_patient(self, patient):
        if patient in self.patients:
            patient.check_vitals()
        else:
            print(f"Error: {patient.name} is not assigned to Dr. {self.name}")

class Patient:
    def __init__(self, name, age, condition):
        self.name = name
        self.age = age
        self.condition = condition
        self.vitals = {"temperature": 37.0, "blood_pressure": "120/80", "heart_rate": 75}
    
    def update_vitals(self, temp, bp, hr):
        self.vitals["temperature"] = temp
        self.vitals["blood_pressure"] = bp
        self.vitals["heart_rate"] = hr
        print(f"Vitals updated for {self.name}")
    
    def check_vitals(self):
        print(f"\nPatient: {self.name} (Age: {self.age})")
        print(f"Condition: {self.condition}")
        print("Current Vitals:")
        print(f"Temperature: {self.vitals['temperature']}°C")
        print(f"Blood Pressure: {self.vitals['blood_pressure']}")
        print(f"Heart Rate: {self.vitals['heart_rate']} bpm")

# Demo the healthcare system
print("\nHealthcare System Demo:")

# Create doctors
Dr_Syah = Doctor("Ahmad", "Cardiologist")
Dr_Sarah = Doctor("Sarah", "Emergency Medicine")

# Create patients
patient1 = Patient("Ali", 45, "Heart Condition")
patient2 = Patient("Maria", 28, "Fever")

# Start on-call shift
Dr_Syah.start_on_call()

# Assign and check patients
Dr_Syah.assign_patient(patient1)
Dr_Sarah.assign_patient(patient2)

# Update and check patient vitals
patient1.update_vitals(38.5, "130/85", 82)
Dr_Syah.check_patient(patient1)

# End on-call shift
Dr_Syah.end_on_call(8)

# Try to check a patient not assigned to the doctor
Dr_Syah.check_patient(patient2)  # This will show an error message

print("\n" + "="*50)
print("DR SYAH's EPIC ON-CALL ADVENTURE!")
print("="*50)

class DoctorSyah:
    def __init__(self):
        self.name = "Dr Syah (BoBoiBoy Mode)"
        self.energy = 100
        self.patients_treated = 0
        self.coffee_power = 30
        self.coffees_left = 3
        self.mood = "fresh"
        
    def treat_patient(self, patient, response_choice):
        print(f"\n🏥 Patient {self.patients_treated + 1}: {patient}")
        
        # Different responses based on player choice
        responses = {
            1: "Baik, jom check tengok apa masalahnya...",
            2: "*Internal screaming* Ok, mari sini...",
            3: "*Contemplates life choices* Ya Allah, give me strength..."
        }
        print(f"Dr Syah: {responses[response_choice]}")
        
        energy_cost = 20
        self.energy -= energy_cost
        self.patients_treated += 1
        
        print(f"\n'{patient}' treated successfully!")
        print(f"Energy depleted: -{energy_cost}")
        print(f"Energy remaining: {self.energy}")
        
        if self.energy < 30:
            print("Dr Syah: *yawns* Ya Allah, penat nya...")
        
    def drink_coffee(self, coffee_type):
        if self.coffees_left > 0:
            print("\n☕ COFFEE TIME!")
            coffee_effects = {
                1: ("Kopi O Kosong", 30),
                2: ("Kopi O Gao", 40),
                3: ("Teh Tarik", 25)
            }
            drink, power = coffee_effects[coffee_type]
            print(f"Dr Syah: Alhamdulillah! {drink} time!")
            
            self.energy += power
            self.coffees_left -= 1
            print(f"Energy restored: +{power}")
            print(f"Energy level: {self.energy}")
            print(f"Coffees remaining: {self.coffees_left}")
        else:
            print("\n❌ NO MORE COFFEE!")
            print("Dr Syah: Ya Allah, habis dah kopi... 😭")

    def check_status(self):
        print(f"\nSTATUS CHECK:")
        print(f"Energy: {self.energy}")
        print(f"Patients treated: {self.patients_treated}")
        print(f"Coffee shots left: {self.coffees_left}")
        
        # Add funny status messages based on energy level
        if self.energy > 80:
            print("Mood: Fresh macam baru mandi! ✨")
        elif self.energy > 50:
            print("Mood: Still surviving... 😊")
        elif self.energy > 30:
            print("Mood: *internally screaming* 😅")
        else:
            print("Mood: Ya Allah, bila nak habis shift ni... 😫")

# List of funny patient cases
patients = [
    "Uncle with 'Emergency' Ingrown Nail (since 2 weeks ago)",
    "Aunty whose BP is high 'because of the weather'",
    "Kid who swallowed his toy car 'because it was hungry'",
    "Teen with 'mysterious' stomach ache (after eating 5 nasi lemak)",
    "Patient who WebMD'd himself into thinking he has everything"
]

# Start the game!
print("\nDr Syah starts his legendary on-call shift!")
print("Can you help Dr Syah survive until the end of his shift?")
dr_syah = DoctorSyah()

for i, patient in enumerate(patients):
    print("\n" + "-"*40)
    dr_syah.check_status()
    
    # Coffee decision
    if dr_syah.energy < 40 and dr_syah.coffees_left > 0:
        print("\nDr Syah looks tired... Need coffee?")
        print("1: Kopi O Kosong (Regular boost)")
        print("2: Kopi O Gao (Extra strong!)")
        print("3: Teh Tarik (Lighter boost)")
        print("4: No thanks, continue working")
        
        try:
            coffee_choice = int(input("Your choice (1-4): "))
            if 1 <= coffee_choice <= 3:
                dr_syah.drink_coffee(coffee_choice)
        except ValueError:
            print("Invalid choice! Continuing without coffee...")
    
    # Response choice for treating patient
    print(f"\nNew patient arrived: {patient}")
    print("How should Dr Syah respond?")
    print("1: Professional and friendly")
    print("2: Tired but maintaining")
    print("3: Internal crisis mode")
    
    try:
        response = int(input("Choose response (1-3): "))
        if not 1 <= response <= 3:
            response = 1
    except ValueError:
        response = 1
    
    dr_syah.treat_patient(patient, response)
    
    if i == len(patients) - 1:
        print("\n🎉 SHIFT COMPLETE!")
        print("Dr Syah: Alhamdulillah! Shift dah habis!")
    elif dr_syah.energy <= 0:
        print("\n💤 DOCTOR DOWN!")
        print("Dr Syah found sleeping in the on-call room...")
        print("Game Over!")
        break

print("\nFINAL STATUS:")
dr_syah.check_status()
if dr_syah.energy > 0:
    print("\nDr Syah successfully survived his on-call shift!")
    print("Achievement Unlocked: BoBoiBoy Doctor Mode Mastered! 🌟")
else:
    print("\nDr Syah needs a very long rest...")
    print("Achievement Unlocked: Found the Comfiest Spot in On-Call Room! 💤")


#Sample
print("Sample Answer")
# 1. Create a simple game character class with health, attack and defend methods
class GameCharacter:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.max_health = health
    
    def attack(self, target):
        damage = 20
        target.health -= damage
        if target.health < 0:
            target.health = 0
        return f"{self.name} attacks {target.name} for {damage} damage!"
    
    def defend(self):
        heal_amount = 10
        self.health += heal_amount
        if self.health > self.max_health:
            self.health = self.max_health
        return f"{self.name} defends and heals for {heal_amount} HP!"
    
    def is_alive(self):
        return self.health > 0
    
    def status(self):
        return f"{self.name}: {self.health}/{self.max_health} HP"

# Create characters
hero = GameCharacter("Hero", 100)
enemy = GameCharacter("Goblin", 80)

# Game simulation
print("=== BATTLE START ===")
print(hero.status())
print(enemy.status())
print()

# Round 1
print(hero.attack(enemy))
print(enemy.status())
print()

# Round 2
print(enemy.attack(hero))
print(hero.status())
print()

# Round 3
print(hero.defend())
print(hero.status())
print()

# Round 4
print(hero.attack(enemy))
print(enemy.status())
print()

# Check if enemy is still alive
if enemy.is_alive():
    print(f"{enemy.name} is still fighting!")
else:
    print(f"{enemy.name} has been defeated!")