/**
 * Cloudflare Pages Functions Middleware
 * Este middleware maneja las peticiones a la API FastAPI
 */

export async function onRequest(context) {
  const { request, env } = context;
  
  // Obtener la URL del backend (configurar en Cloudflare Dashboard)
  const BACKEND_URL = env.BACKEND_URL || 'https://hormiguero.up.railway.app';
  
  // Si la petición es para la API, redirigir al backend
  if (request.url.includes('/api/') || request.url.includes('/docs') || request.url.includes('/health')) {
    const url = new URL(request.url);
    const backendUrl = new URL(BACKEND_URL);
    backendUrl.pathname = url.pathname;
    backendUrl.search = url.search;
    
    const newRequest = new Request(backendUrl.toString(), {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
    
    const response = await fetch(newRequest);
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        ...Object.fromEntries(response.headers),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  }
  
  // Para otras peticiones, continuar normalmente
  return context.next();
}


