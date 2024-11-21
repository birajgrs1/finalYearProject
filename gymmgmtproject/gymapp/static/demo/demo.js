document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("videoFileInput");
    const videoPreview = document.getElementById("videoPreview");
    const analyzeButton = document.getElementById("analyzeButton");
    const resultsSection = document.getElementById("results");
    const processedVideo = document.getElementById("processedVideo");
    const feedbackElement = document.getElementById("feedback");
    const repsCountElement = document.getElementById("repsCount");
    const accuracyElement = document.getElementById("accuracy");
  
    // Handle file selection
    fileInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file && file.type.startsWith("video/")) {
        const videoURL = URL.createObjectURL(file);
        videoPreview.src = videoURL;
        videoPreview.style.display = "block";
        analyzeButton.style.display = "block";
        resultsSection.style.display = "none";
      } else {
        alert("Please select a valid video file.");
        videoPreview.style.display = "none";
        analyzeButton.style.display = "none";
        resultsSection.style.display = "none";
      }
    });
  
    // Analyze button functionality
    analyzeButton.addEventListener("click", (event) => {
      event.preventDefault();
      alert("Analysis started! Processing your video...");
  
      // Simulate processing
      setTimeout(() => {
        const simulatedProcessedVideoURL = videoPreview.src; // Replace with backend processed URL
        processedVideo.src = simulatedProcessedVideoURL;
  
        // Simulated results
        const simulatedFeedback = "Good posture! Keep it up!";
        const simulatedReps = 10;
        const simulatedAccuracy = 85;
  
        feedbackElement.textContent = `Feedback: ${simulatedFeedback}`;
        repsCountElement.textContent = `Reps: ${simulatedReps}`;
        accuracyElement.textContent = `Accuracy: ${simulatedAccuracy}%`;
  
        resultsSection.style.display = "block";
      }, 2000);
    });
  });
  