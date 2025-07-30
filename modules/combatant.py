class Combatant:
    def __init__ (self, name, max_power, power, max_health, health, subterfuge, charisma):
        self.name = name
        self.max_power = max_power
        self.power = power
        self.max_health = max_health
        self.health = health
        self.subterfuge = subterfuge
        self.charisma = charisma

    @classmethod
    def from_string(cls, s: str):
        # Format: "Name, power, max_power, health, max_health, subterfuge, charisma"
        parts = [p.strip() for p in s.split(",")]
        return cls(
            name=parts[0],
            power=int(parts[1]),
            max_power=int(parts[2]),
            health=int(parts[3]),
            max_health=int(parts[4]),
            subterfuge=int(parts[5]),
            charisma=int(parts[6])
        )

    def spend_power(self, amount):
        spend = max(0, min(amount, self.power))
        self.power -= spend
        return spend
    
    def restore_power(self, amount):
        self.power = min(self.max_power, self.power + amount)

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health
    
    def is_alive(self):
        return self.health > 0