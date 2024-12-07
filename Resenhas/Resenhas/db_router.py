class DBRouter():
    
    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'Resenhas':
            return 'DBResenhas'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'Resenhas':
            return 'DBResenhas'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
            if (obj1._meta.db_table == 'Resenhas') or (obj2._meta.db_table == 'Resenhas'):
                return True
            return None
    
    def allow_migrate(self, db, app_label, model_name=None):
        if app_label == 'Resenhas':
            return db == 'DBResenhas'
        return None
