// let menu = document.querySelector('.menu')
// let sidebar = document.querySelector('.sidebar')
// let mainContent = document.querySelector('.main--content')
// menu.onclick = function() {
//     sidebar.classList.toggle('active')
//     mainContent.classList.toggle('active')
// }
console.log("Hello ");
// fetch('/doctors.json') // Ensure this is the correct path

async function fetchDoctorData() {
    try {
        const response = await fetch('../../doctors.json'); // Ensure the path is correct
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();

        // Assuming you have a way to identify the logged-in doctor
         // Use the loggedInDoctorEmail variable set from Flask
         const currentDoctor = data.find(doctor => doctor.email === loggedInDoctorEmail);
        
        if (currentDoctor) {
            displayDoctorAnalytics(currentDoctor);
        } else {
            console.error('Doctor not found');
        }
    } catch (error) {
        console.error('Error fetching doctor data:', error);
    }
}

function displayDoctorAnalytics(doctor) {
    // Example: Display doctor name and appointments count
    const appointments = doctor.appointments || [];
    const appointmentCount = appointments.length;

    // Update appointment count for "Register New Patient" card
    document.querySelector('.card-2 h1').innerText = appointmentCount; // Update with appointment count

    // Initialize pending and completed counts
    let pendingCount =  appointmentCount;
    let completedCount = 0;

    // Check appointments and update counts
    if (appointments.length === 0) {
        // No appointments found, set defaults
        pendingCount =  appointmentCount; // No pending patients
        completedCount = 0; // No completed patients
    } else {
        appointments.forEach(appointment => {
            // Logic to determine if appointment is pending or completed
            if (appointment.status === 'Pending') {
                pendingCount++;
            } else if (appointment.status === 'Completed') {
                completedCount++;
            }
        });
    }

    // Update the pending and completed counts on the dashboard
    document.querySelector('.card-3 h1').innerText = pendingCount; // Update Pending count
    document.querySelector('.card-4 h1').innerText = completedCount; // Update Completed count

    // Populate recent patients table
    const recentPatientsTableBody = document.querySelector('.recent--patients tbody');
    recentPatientsTableBody.innerHTML = ''; // Clear existing rows

    if (appointments.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="5">No appointments available</td>
        `;
        recentPatientsTableBody.appendChild(row);
    } else {
        appointments.forEach(appointment => {
            const row = document.createElement('tr');
            const patientId = appointment.patient_id; // Assuming patient_id can be used for display
            row.innerHTML = `
                <td>${patientId}</td>
                <td>${appointment.day}</td>
                <td>${appointment.time_slot}</td>
                <td>${appointment.status}</td> <!-- Update with actual status -->
                <td><span><i class="ri-edit-line edit"></i><i class="ri-delete-bin-line delete"></i></span></td>
            `;
            recentPatientsTableBody.appendChild(row);
        });
    }
}



// Call the fetch function on page load or appropriate event
fetchDoctorData();


// document.addEventListener("DOMContentLoaded", function () {
//     fetch("../../doctors.json")
//         .then(response => response.json())
//         .then(data => {
//             const doctor = data;
//             const appointments = doctor.appointments;

//             // Update overview section dynamically
//             document.getElementById("new-patient-count").innerText = appointments.length;
//             document.getElementById("total-patient-count").innerText = appointments.length; // You can use another value for this based on total patients
//             document.getElementById("my-schedule-count").innerText = appointments.length;
//             document.getElementById("completed-patient-count").innerText = appointments.filter(a => a.status === 'completed').length;

//             // For simplicity, set static percentages or calculate them dynamically if you have the data
//             document.getElementById("new-patient-percentage").innerText = 65;
//             document.getElementById("total-patient-percentage").innerText = 82;
//             document.getElementById("schedule-percentage").innerText = 27;
//             document.getElementById("completed-patient-percentage").innerText = 8;

//             // Populate the patient table
//             const patientTableBody = document.getElementById("patient-table-body");
//             patientTableBody.innerHTML = ''; // Clear any existing rows

//             appointments.forEach(appointment => {
//                 const patientRow = document.createElement("tr");

//                 // You might need to fetch patient details using `appointment.patient_id` in a real app
//                 patientRow.innerHTML = `
//                     <td>${appointment.patient_id}</td>
//                     <td>${appointment.day}</td>
//                     <td>${appointment.gender || 'Unknown'}</td>
//                     <td>${appointment.age || 'N/A'}</td>
//                     <td class="${appointment.status || 'pending'}">${appointment.status || 'Pending'}</td>
//                     <td><span><i class="ri-edit-line edit"></i><i class="ri-delete-bin-line delete"></i></span></td>
//                 `;

//                 patientTableBody.appendChild(patientRow);
//             });
//         })
//         .catch(error => console.error('Error fetching doctor data:', error));
// });
