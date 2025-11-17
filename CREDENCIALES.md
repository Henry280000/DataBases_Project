# CREDENCIALES DE ACCESO - PHARMAFLOW SOLUTIONS

## Usuarios del Sistema

Cada usuario ahora tiene su propia contraseña única:

### Gerente
- **Usuario:** `admin_gerente`
- **Contraseña:** `Admin2024!`
- **Nombre:** Carlos Mendoza Ruiz
- **Email:** carlos.mendoza@pharmaflow.com

### Farmacéuticos
1. **María García**
   - **Usuario:** `maria_farm`
   - **Contraseña:** `Maria2024!`
   - **Email:** maria.garcia@pharmaflow.com

2. **José Rodríguez**
   - **Usuario:** `jose_farm`
   - **Contraseña:** `Jose2024!`
   - **Email:** jose.rodriguez@pharmaflow.com

### Investigadores
1. **Ana Martínez**
   - **Usuario:** `ana_investigadora`
   - **Contraseña:** `Ana2024!`
   - **Email:** ana.martinez@pharmaflow.com

2. **Luis Hernández**
   - **Usuario:** `luis_investigador`
   - **Contraseña:** `Luis2024!`
   - **Email:** luis.hernandez@pharmaflow.com

## Acceso al Sistema

- **URL Local:** http://127.0.0.1:5001
- **URL Red:** http://10.100.80.123:5001

## Funcionalidades del Login

1. **Formulario sin JavaScript**: El login funciona con POST tradicional
2. **Botón mostrar/ocultar contraseña**: Haz clic en el icono para ver la contraseña
3. **Validación de contraseñas con bcrypt**: Todas las contraseñas están encriptadas de forma segura
4. **Contraseñas únicas**: Cada usuario tiene su propia contraseña personalizada

## Seguridad

- Todas las contraseñas están hasheadas con bcrypt (12 rounds)
- Cada usuario tiene un hash único
- Las contraseñas nunca se almacenan en texto plano
- Validación del lado del servidor
