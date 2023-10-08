from quart import current_app

from anunnaki_server.model import Extension

from typing import List, Tuple
from aiosqlite import Connection

async def db_execute(query: str, args: Tuple = None) -> bool:
    """Execute SQLite query and report success"""
    db: Connection = current_app.sqlite_db
    try:
        await db.execute(query, args)
        await db.commit()
    except:
        return False
    else:
        return True

async def extensions_list() -> List[Extension]:
    """Get all of the installed extensions"""
    db: Connection = current_app.sqlite_db
    cur = await db.execute("SELECT * FROM extensions")
    extensions = await cur.fetchall()
    return [Extension(installed=True, **extension) for extension in extensions]

async def extension_add(ext: Extension) -> bool:
    """Add new extension row to the database table"""
    query = f'''INSERT INTO extensions(id, pkg, name, lang, version, base_url) 
            VALUES (?, ?, ?, ?, ?, ?)'''
    args = (ext.id, ext.pkg, ext.name, ext.lang, ext.version, ext.base_url)
    
    return await db_execute(query, args)
    
async def extension_update(ext: Extension) -> bool:
    """Update extension row with the new data"""
    query = f'''UPDATE extensions SET pkg = ?, name = ?, lang = ?,
             version = ?, base_url = ? WHERE id = ?'''
    args = (ext.pkg, ext.name, ext.lang, ext.version, ext.base_url, ext.id)

    return await db_execute(query, args)

async def extension_remove(ext: Extension) -> bool:
    """Remove extension row from the database table"""
    query = '''DELETE FROM extensions WHERE id=?'''
    args = (ext.id,)

    return await db_execute(query, args)