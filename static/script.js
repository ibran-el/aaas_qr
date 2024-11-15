    // Initialize the QR code scanner
    const html5QrCode = new Html5Qrcode("reader");

    // Function to start scanning
    function startScanning() {

        const rollcallInput = document.getElementById('rollcall_for');
        const rollcall_for = rollcallInput.value; // Get the selected value
        
        // Check if rollcall_for is valid (not the placeholder option)
        if (!rollcall_for || rollcall_for == "rollcall for") {
            alert("Please select a valid 'rollcall for' option before scanning.");
            return; // Stop execution if invalid
        }

        const config = { fps: 120, qrbox: 250 }; // Configuration for scanning

        // Start the scanning process
        html5QrCode.start(
            { facingMode: "environment" }, // Use the back camera
            config,
            (decodedText, decodedResult) => { // Success callback
               
                console.log(`QR Code detected: ${decodedText}`);

                 // Redirect to a specific URL with the decoded text as a query parameter

                //  const redirectUrl = `/mark_attendance/${decodedText}`;
                //  window.location.href = redirectUrl; // Redirect to the new URL


                // Extract the part after 'STUDENT ID'
                const admissionNo = decodedText.split('STUDENT ID')[1].trim();  // This should give 'AS/2024/0010'


                // Construct the redirect URL
                const redirectUrl = `https://aaas-qr.onrender.com/mark_attendance/${admissionNo}?rollcall_for=${rollcall_for}`;
                

                // Redirect to the new URL
                window.location.href = redirectUrl;
                
                html5QrCode.stop(); // Stop scanning after successful detection
            },
            (errorMessage) => { 
                // Optional: Handle scan errors here
                console.warn(`QR Code scan error: ${errorMessage}`);
            }
        ).catch(err => {
            console.error(`Error starting QR code scanner: ${err}`);
        });

        // Hide the  Start button after starting the scan
        document.getElementById("startScanButton").style.display = 'none';

        // Show the Stop  button after stopping the scan
        document.getElementById("StopScanning").style.display = 'inline';
    }

    function stopScanning(){
        html5QrCode.stop();
        // Show the  Start button after starting the scan
        document.getElementById("startScanButton").style.display = 'inline';

        // Hide the Stop  button after stopping the scan
        document.getElementById("StopScanning").style.display = 'none';
    }

    // Start scanning when the page loads
    // window.onload = startScanning;
    document.getElementById("startScanButton").addEventListener("click", startScanning);
    document.getElementById("StopScanning").addEventListener("click", stopScanning);

