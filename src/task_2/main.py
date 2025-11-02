from pymongo import MongoClient
from bson import ObjectId

try:
  client = MongoClient("mongodb://admin:password123@localhost:27017/")
  # Check connection
  client.admin.command('ping')
  print("✅ Successfully connected to MongoDB")
  
  db = client["cats_database"]
  collection = db["cats"]
except Exception as e:
  print(f"❌ MongoDB connection error: {e}")
  exit(1)

def create_cat(name: str, age: int, features: list):
  """Create new cat in the collection"""
  try:
    # Check if cat already exists
    if collection.find_one({"name": name}):
      print(f"❌ Cat with name '{name}' already exists!")
      return None
      
    cat = {
      "name": name,
      "age": age,
      "features": features
    }
    
    result = collection.insert_one(cat)
    print(f"✅ Created cat with id: {result.inserted_id}")
    return result.inserted_id
  except Exception as e:
    print(f"❌ Error creating cat: {e}")
    return None

def read_all_cats():
  """Read all cats from the collection"""
  try:
    cats = list(collection.find())
    if cats:
      print(f"📋 Found {len(cats)} cats:")
      for cat in cats:
        print(f"  - {cat['name']}, {cat['age']} years: {cat['features']}")
    else:
      print("📋 No cats found in database")
    return cats
  except Exception as e:
    print(f"❌ Error reading cats: {e}")
    return []

def read_cat_by_name(name: str):
  """Read cat by name from the collection"""
  try:
    cat = collection.find_one({"name": name})
    if cat:
      print(f"🐱 Found cat: {cat['name']}, {cat['age']} years: {cat['features']}")
      return cat
    else:
      print(f"❌ Cat with name '{name}' not found")
      return None
  except Exception as e:
    print(f"❌ Error searching for cat: {e}")
    return None

def update_cat_age(cat_name: str, new_age: int):
  """Update cat's age by name"""
  try:
    result = collection.update_one(
      {"name": cat_name},
      {"$set": {"age": new_age}}
    )
    
    if result.matched_count > 0:
      print(f"✅ Updated age for {cat_name} to {new_age}")
    else:
      print(f"❌ Cat with name '{cat_name}' not found")
    
    return result
  except Exception as e:
    print(f"❌ Error updating cat's age: {e}")
    return None

def update_cat_features(cat_name: str, new_features: list):
  """Update cat's features by name"""
  try:
    # get current features
    cat = collection.find_one({"name": cat_name})
    if not cat:
      print(f"❌ Cat with name '{cat_name}' not found")
      return None
      
    current_features = cat.get("features", [])

    # add new features to current features
    updated_features = list(set(current_features + new_features))

    # update in db
    result = collection.update_one(
      {"name": cat_name},
      {"$set": {"features": updated_features}}
    )

    print(f"✅ Updated features for {cat_name} to {updated_features}")
    return result
  except Exception as e:
    print(f"❌ Error updating cat's features: {e}")
    return None 

def delete_cat(cat_name: str):
  """Delete cat by name from the collection"""
  try:
    result = collection.delete_one({"name": cat_name})
    
    if result.deleted_count > 0:
      print(f"✅ Deleted cat: {cat_name}")
    else:
      print(f"❌ Cat with name '{cat_name}' not found")
    
    return result
  except Exception as e:
    print(f"❌ Error deleting cat: {e}")
    return None

def delete_all_cats():
  """Delete all cats from the collection"""
  try:
    result = collection.delete_many({})
    print(f"✅ Deleted {result.deleted_count} cats")
    return result
  except Exception as e:
    print(f"❌ Error deleting all cats: {e}")
    return None

if __name__ == "__main__":
  # create cats
  create_cat("Whiskers", 3, ["playful", "curious"])
  create_cat("Mittens", 5, ["lazy", "affectionate"])

  # read all cats
  read_all_cats()

  # read cat by name
  read_cat_by_name("Whiskers")

  # update cat age
  update_cat_age("Mittens", 6)

  # update cat features
  update_cat_features("Whiskers", ["independent", "playful"])

  # delete cat by name
  delete_cat("Mittens")
