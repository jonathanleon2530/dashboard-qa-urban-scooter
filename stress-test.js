import http from 'k6/http';
import { sleep, check } from 'k6';

// Configuración de la carga
export const options = {
    stages: [
        { duration: '30s', target: 20 }, // Subir a 20 usuarios en 30s
        { duration: '1m', target: 20 }, // Mantener 20 usuarios por 1 minuto
        { duration: '20s', target: 0 }, // Bajar a 0 usuarios
    ],
};

export default function() {
    // URL de ParaBank que vimos en tu Swagger
    const url = 'https://parabank.parasoft.com/parabank/services/bank/billpay?accountId=13579';

    const payload = JSON.stringify({
        "name": "Test User",
        "address": {
            "street": "Calle 60",
            "city": "Mérida",
            "state": "Yucatán",
            "zipCode": "97000"
        },
        "phoneNumber": "9991234567",
        "accountNumber": 54321,
        "amount": 10.00
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const res = http.post(url, payload, params);

    // Verificaciones de QA
    check(res, {
        'status es 200': (r) => r.status === 200,
        'tiempo de respuesta < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);
}