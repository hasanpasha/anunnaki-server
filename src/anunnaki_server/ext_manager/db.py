from quart import g

from anunnaki_server.model import Extension

from typing import List, Tuple
from sqlite3 import Connection

def db_execute(query: str, args: Tuple = None) -> bool:
    """Execute SQLite query and report success"""
    db: Connection = g.sqlite_db
    try:
        cur = db.execute(query, args)
        db.commit()
    except:
        return False
    else:
        return True

def extensions_list() -> List[Extension]:
    """Get all of the installed extensions"""
    db: Connection = g.sqlite_db
    cur = db.execute("SELECT * FROM extensions")
    extensions = cur.fetchall()
    return [Extension(installed=True, **extension) for extension in extensions]

def extension_add(ext: Extension) -> bool:
    """Add new extension row to the database table"""
    query = f'''INSERT INTO extensions(id, pkg, name, lang, version, base_url) 
            VALUES (?, ?, ?, ?, ?, ?)'''
    args = (ext.id, ext.pkg, ext.name, ext.lang, ext.version, ext.base_url)
    
    return db_execute(query, args)
    
def extension_update(ext: Extension) -> bool:
    """Update extension row with the new data"""
    query = f'''UPDATE extensions SET pkg = ?, name = ?, lang = ?,
             version = ?, base_url = ? WHERE id = ?'''
    args = (ext.pkg, ext.name, ext.lang, ext.version, ext.base_url, ext.id)

    return db_execute(query, args)

def extension_remove(ext: Extension) -> bool:
    """Remove extension row from the database table"""
    query = '''DELETE FROM extensions WHERE id=?'''
    args = (ext.id,)

    return db_execute(query, args)