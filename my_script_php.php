<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Verificar que se hayan seleccionado las imágenes
    if (!empty($_FILES['image1']) && !empty($_FILES['image2'])) {
        // Obtener los datos de las imágenes seleccionadas
        $image1_data = base64_encode(file_get_contents($_FILES['image1']['tmp_name']));
        $image2_data = base64_encode(file_get_contents($_FILES['image2']['tmp_name']));
        
        // Crear un arreglo JSON con las imágenes codificadas en base64
        $data = array(
            'image1' => $image1_data,
            'image2' => $image2_data
        );
        
        // URL de tu API
        $url = 'http://localhost:8000/upload/'; // Asegúrate de reemplazar con la URL correcta de tu API
        
        // Configurar la solicitud POST
        $options = array(
            'http' => array(
                'header' => "Content-Type: application/json\r\n",
                'method' => 'POST',
                'content' => json_encode($data)
            )
        );
        
        $context = stream_context_create($options);
        
        // Realizar la solicitud POST
        $response = file_get_contents($url, false, $context);
        
        // Imprimir la respuesta de la API
        echo "Response: " . $response;
    } else {
        echo "Por favor, selecciona ambas imágenes.";
    }
}

?>