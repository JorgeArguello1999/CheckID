<!DOCTYPE html>
<html>
<head>
    <title>Subir Imágenes con Previsualización</title>
    <script>
        function mostrarImagen(input, imgElement) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    imgElement.src = e.target.result;
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
    </script>
    <style>
        /* Estilos para centrar el div 'form' */
        .form {
            text-align: center;
        }

        /* Estilos para los divs 'form-1' y 'form-2' */
        .form-1,
        .form-2 {
            display: inline-block; /* Mostrar los divs en línea uno al lado del otro */
            margin: 10px; /* Agregar margen entre ellos para separación */
            border: dashed;
            padding: 1em;
        }

        /* Estilos para las imágenes de previsualización */
        img {
            max-width: 200px;
            max-height: 200px;
        }
    </style>
</head>

<body>
    <h1>Subir Imágenes con Previsualización</h1>
    <div class="form">
        <form action="" method="post" enctype="multipart/form-data">
            <div class="form-1">
                <input type="file" name="image1" id="image1" accept="image/jpeg" required onchange="mostrarImagen(this, preview1)">
                <br>
                <img src="" alt="" id="preview1" style="max-width: 200px; max-height: 200px;">
            </div>

            <div class="form-2">
                <input type="file" name="image2" id="image2" accept="image/jpeg" required onchange="mostrarImagen(this, preview2)">
                <br>
                <img src="" alt="" id="preview2" style="max-width: 200px; max-height: 200px;">
            </div>

            <label for=""></label>
            <input name="cedula" type="text">
            <br>
            <input type="submit" value="Subir Imágenes">

        </form>
    </div>
</body>
</html>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Verificar que se hayan seleccionado las imágenes
    if (!empty($_FILES['image1']) && !empty($_FILES['image2'])) {
        // Obtener los datos de las imágenes seleccionadas
        $image1_data = base64_encode(file_get_contents($_FILES['image1']['tmp_name']));
        $image2_data = base64_encode(file_get_contents($_FILES['image2']['tmp_name']));
        $cedula = $_POST["cedula"];
        
        // Crear un arreglo JSON con las imágenes codificadas en base64
        $data = array(
            'image1' => $image1_data,
            'image2' => $image2_data,
            'cedula' => $cedula
        );
        
        // URL de tu API
        $url = 'http://localhost:8000/upload/'; // Asegúrate de reemplazar con la URL correcta de tu API
        // $url = "https://8000-cs-d00e4d77-a974-4e76-84af-d83f2279f3f7.cs-us-west1-wolo.cloudshell.dev/upload/";
        
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
        echo $response;
        
    } else {
        echo "Por favor, selecciona ambas imágenes.";
    }
}
?>
