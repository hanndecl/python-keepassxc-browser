from pathlib import Path

from keepassxc_browser import Connection, Identity

client_id = 'python-keepassxc-browser'

state_file = Path('.assoc')
if state_file.exists():
    with state_file.open('r') as f:
        data = f.read()
    browser_id = Identity.unserialize(client_id, data)
else:
    browser_id = Identity(client_id)

c = Connection()
c.connect()
c.change_public_keys(browser_id)
c.get_database_hash(browser_id)

if not c.test_associate(browser_id):
    associated_name = c.associate(browser_id)
    assert c.test_associate(browser_id)
    data = browser_id.serialize()
    with state_file.open('w') as f:
        f.write(data)
    del data

c.create_password(browser_id)
c.set_login(browser_id, url='https://python-test123', login='test-user', password='test-password', entry_id=None,
            submit_url=None)
result = c.get_logins(browser_id, url='https://python-test123')
assert "test-password" == result[0]["password"]
# c.lock_database(id)
c.disconnect()
