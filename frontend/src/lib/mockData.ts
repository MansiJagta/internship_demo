export interface Vehicle {
  id: string;
  make: string;
  model: string;
  year: number;
  price: number;
  mileage: number;
  image: string;
  images: string[];
  fuel_type: string;
  transmission: string;
  engine: string;
  horsepower: number;
  drivetrain: string;
  exterior_color: string;
  interior_color: string;
  mpg_city: number;
  mpg_highway: number;
  description: string;
  is_anomaly: boolean;
  anomaly_severity?: "high" | "medium";
  seller: string;
  location: string;
  listed_date: string;
  vin: string;
}

export interface Offer {
  id: string;
  vehicle_id: string;
  vehicle_title: string;
  vehicle_image: string;
  offer_price: number;
  asking_price: number;
  status: "pending" | "accepted" | "countered" | "rejected";
  counter_price?: number;
  created_at: string;
  updated_at: string;
  messages: ChatMessage[];
}

export interface ChatMessage {
  id: string;
  sender: "user" | "ai";
  message: string;
  timestamp: string;
}

const carImages = [
  "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80",
  "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80",
  "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&q=80",
  "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
  "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80",
  "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
  "https://images.unsplash.com/photo-1616422285623-13ff0162193c?w=800&q=80",
  "https://images.unsplash.com/photo-1542362567-b07e54358753?w=800&q=80",
];

export const vehicles: Vehicle[] = [
  {
    id: "1", make: "Tesla", model: "Model S Plaid", year: 2024, price: 89990, mileage: 1200,
    image: carImages[0], images: [carImages[0], carImages[1], carImages[2]],
    fuel_type: "Electric", transmission: "Single-Speed", engine: "Tri Motor AWD", horsepower: 1020,
    drivetrain: "AWD", exterior_color: "Pearl White", interior_color: "Black",
    mpg_city: 124, mpg_highway: 115, description: "Pristine condition with Full Self-Driving capability.",
    is_anomaly: false, seller: "AutoVibe Certified", location: "San Francisco, CA",
    listed_date: "2024-12-01", vin: "5YJSA1E61MF000001",
  },
  {
    id: "2", make: "BMW", model: "M4 Competition", year: 2023, price: 12500, mileage: 8500,
    image: carImages[1], images: [carImages[1], carImages[3], carImages[4]],
    fuel_type: "Gasoline", transmission: "8-Speed Automatic", engine: "3.0L Twin-Turbo I6", horsepower: 503,
    drivetrain: "RWD", exterior_color: "Isle of Man Green", interior_color: "Cognac",
    mpg_city: 16, mpg_highway: 23, description: "Low mileage M4 Competition in rare color.",
    is_anomaly: true, anomaly_severity: "high", seller: "Private Seller", location: "Miami, FL",
    listed_date: "2024-11-28", vin: "WBS43AZ02PCL00002",
  },
  {
    id: "3", make: "Porsche", model: "911 GT3", year: 2023, price: 179900, mileage: 3200,
    image: carImages[2], images: [carImages[2], carImages[5], carImages[6]],
    fuel_type: "Gasoline", transmission: "7-Speed PDK", engine: "4.0L Flat-6", horsepower: 502,
    drivetrain: "RWD", exterior_color: "Shark Blue", interior_color: "Black",
    mpg_city: 15, mpg_highway: 20, description: "Track-ready 911 GT3 with sport exhaust.",
    is_anomaly: false, seller: "Porsche Certified", location: "Los Angeles, CA",
    listed_date: "2024-12-05", vin: "WP0AC2A97PS200003",
  },
  {
    id: "4", make: "Mercedes-Benz", model: "AMG GT 63", year: 2024, price: 145000, mileage: 500,
    image: carImages[3], images: [carImages[3], carImages[7], carImages[0]],
    fuel_type: "Gasoline", transmission: "9-Speed Automatic", engine: "4.0L Twin-Turbo V8", horsepower: 577,
    drivetrain: "AWD", exterior_color: "Obsidian Black", interior_color: "Red Pepper",
    mpg_city: 16, mpg_highway: 22, description: "Nearly new AMG GT 63 with all options.",
    is_anomaly: false, seller: "MB Dealer", location: "New York, NY",
    listed_date: "2024-12-10", vin: "W1KCG5DB0RA000004",
  },
  {
    id: "5", make: "Audi", model: "RS e-tron GT", year: 2024, price: 28000, mileage: 45000,
    image: carImages[4], images: [carImages[4], carImages[1], carImages[6]],
    fuel_type: "Electric", transmission: "2-Speed Automatic", engine: "Dual Motor", horsepower: 637,
    drivetrain: "AWD", exterior_color: "Daytona Gray", interior_color: "Black",
    mpg_city: 79, mpg_highway: 82, description: "Performance EV with premium package. Suspiciously low price for year/model.",
    is_anomaly: true, anomaly_severity: "medium", seller: "Unknown Dealer", location: "Phoenix, AZ",
    listed_date: "2024-12-03", vin: "WUAESAF17NA000005",
  },
  {
    id: "6", make: "Lamborghini", model: "Huracán EVO", year: 2022, price: 269000, mileage: 6800,
    image: carImages[5], images: [carImages[5], carImages[2], carImages[7]],
    fuel_type: "Gasoline", transmission: "7-Speed DCT", engine: "5.2L V10", horsepower: 631,
    drivetrain: "AWD", exterior_color: "Verde Mantis", interior_color: "Nero Ade",
    mpg_city: 13, mpg_highway: 18, description: "Stunning Huracán EVO in iconic green.",
    is_anomaly: false, seller: "Exotic Motors", location: "Las Vegas, NV",
    listed_date: "2024-11-20", vin: "ZHWUF4ZF3NLA00006",
  },
  {
    id: "7", make: "Ford", model: "Mustang GT", year: 2024, price: 42500, mileage: 2100,
    image: carImages[6], images: [carImages[6], carImages[0], carImages[3]],
    fuel_type: "Gasoline", transmission: "6-Speed Manual", engine: "5.0L Coyote V8", horsepower: 486,
    drivetrain: "RWD", exterior_color: "Vapor Blue", interior_color: "Ebony",
    mpg_city: 15, mpg_highway: 24, description: "New generation Mustang GT with Performance Pack.",
    is_anomaly: false, seller: "Ford Certified", location: "Detroit, MI",
    listed_date: "2024-12-08", vin: "1FA6P8CF0R5R00007",
  },
  {
    id: "8", make: "Rivian", model: "R1T Adventure", year: 2024, price: 73000, mileage: 4500,
    image: carImages[7], images: [carImages[7], carImages[4], carImages[1]],
    fuel_type: "Electric", transmission: "Single-Speed", engine: "Quad Motor", horsepower: 835,
    drivetrain: "AWD", exterior_color: "Forest Green", interior_color: "Ocean Coast",
    mpg_city: 73, mpg_highway: 65, description: "Adventure-ready electric truck with camping gear package.",
    is_anomaly: false, seller: "Rivian Direct", location: "Seattle, WA",
    listed_date: "2024-12-12", vin: "7FCTGAAL5NN000008",
  },
];

export const offers: Offer[] = [
  {
    id: "o1", vehicle_id: "1", vehicle_title: "2024 Tesla Model S Plaid",
    vehicle_image: carImages[0], offer_price: 82000, asking_price: 89990,
    status: "countered", counter_price: 86500,
    created_at: "2024-12-10T10:30:00Z", updated_at: "2024-12-11T14:20:00Z",
    messages: [
      { id: "m1", sender: "user", message: "I'd like to offer $82,000 for this Model S.", timestamp: "2024-12-10T10:30:00Z" },
      { id: "m2", sender: "ai", message: "Thank you for your offer. The seller has countered at $86,500, noting the low mileage and FSD capability.", timestamp: "2024-12-11T14:20:00Z" },
    ],
  },
  {
    id: "o2", vehicle_id: "7", vehicle_title: "2024 Ford Mustang GT",
    vehicle_image: carImages[6], offer_price: 39000, asking_price: 42500,
    status: "pending",
    created_at: "2024-12-12T09:15:00Z", updated_at: "2024-12-12T09:15:00Z",
    messages: [
      { id: "m3", sender: "user", message: "Would you accept $39,000?", timestamp: "2024-12-12T09:15:00Z" },
    ],
  },
  {
    id: "o3", vehicle_id: "3", vehicle_title: "2023 Porsche 911 GT3",
    vehicle_image: carImages[2], offer_price: 170000, asking_price: 179900,
    status: "accepted",
    created_at: "2024-12-08T16:00:00Z", updated_at: "2024-12-09T11:45:00Z",
    messages: [
      { id: "m4", sender: "user", message: "Offering $170,000 for the GT3.", timestamp: "2024-12-08T16:00:00Z" },
      { id: "m5", sender: "ai", message: "Congratulations! The seller has accepted your offer of $170,000. We'll be in touch with next steps.", timestamp: "2024-12-09T11:45:00Z" },
    ],
  },
];
