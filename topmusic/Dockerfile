# Imagen base
FROM node:20

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos y dependencias
COPY package.json package-lock.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Exponer el puerto del frontend
EXPOSE 3000

# Comando para ejecutar la app en un servidor web
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
