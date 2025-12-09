# ──────────────────────────────────────────────────────────────
# FIXED & SUPER FAST – uses Debian instead of Alpine (no rollup bug)
# ──────────────────────────────────────────────────────────────
FROM node:20-bullseye-slim as build

WORKDIR /app

# Copy only package files first (better caching)
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Now copy source code
COPY . .

# Build the React app
RUN npm run build -- --mode production

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80