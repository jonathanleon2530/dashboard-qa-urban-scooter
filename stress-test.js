import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Configuración de la carga (Escenarios)
export const options = {
    stages: [
        { duration: '1m', target: 50 }, // Rampa de subida: de 0 a 50 usuarios en 1 min
        { duration: '3m', target: 50 }, // Meseta: mantener 50 usuarios por 3 min
        { duration: '1m', target: 200 }, // Pico de estrés: subir a 200 usuarios de golpe
        { duration: '2m', target: 0 }, // Rampa de bajada: recuperación del sistema
    ],
    thresholds: {
        http_req_failed: ['rate<0.01'], // El error debe ser menor al 1%
        http_req_duration: ['p(95)<500'], // El 95% de las peticiones deben tardar < 500ms
    },
};

// 2. Lógica de la prueba
export default function() {
    // Simula una consulta a un endpoint de préstamos o productos
    const res = http.get('https://test-api.k6.io/public/crocodiles/');

    check(res, {
        'status es 200': (r) => r.status === 200,
        'tiempo de respuesta aceptable': (r) => r.timings.duration < 600,
    });

    sleep(1); // Simula el tiempo que tarda un usuario real entre clics
}