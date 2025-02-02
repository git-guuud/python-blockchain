import plyvel

db = plyvel.DB('testdb', create_if_missing=True)
db.put(b'key', b'value')

print(db.get(b'key').decode())