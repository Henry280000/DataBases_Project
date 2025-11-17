from pymongo.errors import PyMongoError
from datetime import datetime
from bson import ObjectId


class MongoDBModels:        
    def __init__(self, database):
        self.db = database
        
        # Referencia a colección única
        if self.db is not None:
            self.clinical_trials = self.db.clinical_trials
    
    def _serialize_doc(self, doc):
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    
    def _serialize_docs(self, docs):
        return [self._serialize_doc(doc) for doc in docs]
    
    # ENSAYOS CLÍNICOS
    
    def get_all_clinical_trials(self):
        try:
            trials = list(self.clinical_trials.find().sort('fecha_inicio', -1))
            return self._serialize_docs(trials)
        except PyMongoError as e:
            print(f"Error obteniendo ensayos clínicos: {e}")
            return []
    
    def get_clinical_trial_by_id(self, trial_id):
        try:
            trial = self.clinical_trials.find_one({'trial_id': trial_id})
            return self._serialize_doc(trial)
        except PyMongoError as e:
            print(f"Error obteniendo ensayo clínico: {e}")
            return None
    
    def create_clinical_trial(self, data):
        try:
            # Agregar metadatos
            data['metadata'] = {
                'fecha_creacion': datetime.now(),
                'fecha_modificacion': datetime.now(),
                'version': 1
            }
            
            # Validar campos requeridos
            required = ['trial_id', 'titulo', 'medicamento_id', 'fase', 
                       'fecha_inicio', 'estado']
            if not all(field in data for field in required):
                return {'success': False, 'mensaje': 'Datos incompletos'}
            
            # Convertir fecha de string a datetime si es necesario
            if isinstance(data['fecha_inicio'], str):
                data['fecha_inicio'] = datetime.fromisoformat(data['fecha_inicio'])
            
            if 'fecha_finalizacion' in data and isinstance(data['fecha_finalizacion'], str):
                data['fecha_finalizacion'] = datetime.fromisoformat(data['fecha_finalizacion'])
            
            result = self.clinical_trials.insert_one(data)
            
            return {
                'success': True,
                'trial_id': data['trial_id'],
                '_id': str(result.inserted_id)
            }
        
        except PyMongoError as e:
            return {'success': False, 'mensaje': str(e)}
    
    def update_clinical_trial(self, trial_id, data):
        try:
            # Actualizar metadata
            data['metadata.fecha_modificacion'] = datetime.now()
            
            # Incrementar versión
            self.clinical_trials.update_one(
                {'trial_id': trial_id},
                {'$inc': {'metadata.version': 1}}
            )
            
            result = self.clinical_trials.update_one(
                {'trial_id': trial_id},
                {'$set': data}
            )
            
            if result.modified_count > 0:
                return {'success': True}
            else:
                return {'success': False, 'mensaje': 'No se encontró el ensayo'}
        
        except PyMongoError as e:
            return {'success': False, 'mensaje': str(e)}
