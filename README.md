# Darshan Doot Ticket Booking System

Darshan Doot is an innovative multilingual chatbot-based ticketing system designed to enhance the visitor experience in museums by streamlining the ticket booking process. Recognizing the challenges traditional manual ticketing systems pose—such as long queues, inefficient operations, and human errors—our solution leverages advanced technology to create a seamless, efficient, and user-friendly platform.

## Table of Contents

- [Introduction](#introduction)
- [Planned Features](#planned-features)
- [System Architecture](#system-architecture)
- [Impact and Benefits](#impact-and-benefits)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Credits](#credits)


## Introduction

The Darshan Doot Ticket Booking System is designed to transform the museum visitor experience by addressing the inefficiencies of traditional ticket booking methods. By leveraging advanced natural language processing with Botpress NLU, the system enables users to book tickets seamlessly through WhatsApp, enhancing accessibility and convenience.

Promotion video: [View on Youtube](https://www.youtube.com/watch?v=OPNlICShREI)

## Planned Features

1. **Multilingual Support**: The chatbot supports multiple languages, making it accessible to a diverse audience and improving user engagement.
2. **Natural Language Processing**: Utilizing Botpress NLU, the system understands user intents through example-driven training, enabling accurate responses and a more natural interaction.
3. **WhatsApp Integration**: By using the WhatsApp API, users can easily book tickets directly from their mobile devices, enhancing convenience and accessibility.
4. **Payment Integration**: The system integrates with Stripe to offer a wide range of payment options, including cards, vouchers, and country-specific payment methods, ensuring a smooth transaction process.
5. **Advanced Ticketing Features**: Our platform allows for group bookings with unique QR codes for up to six members, reducing queue times and improving efficiency during peak hours.
6. **Data Analytics**: By collecting and analyzing visitor data, the system provides valuable insights into user behavior and preferences, aiding in decision-making and targeted marketing efforts.
7. **Robust Backend**: Built on Django and supported by MySQL and PostgreSQL databases, the system ensures rapid development, reliability, and efficient data management. Redis is used for caching frequently accessed data, optimizing performance.
8. **Scalability**: The solution utilizes Docker for containerization and Kubernetes for orchestration, ensuring scalability and high uptime to handle varying volumes of traffic.
9. **Security and Monitoring**: The implementation follows best security practices and utilizes Google Analytics for real-time performance monitoring, ensuring a safe user experience.

## System Architecture

The system architecture of Darshan Doot is designed to ensure scalability, reliability, and efficiency. Below is a diagram illustrating the architecture:

![System Architecture](/System_Arch.png)


## Impact and Benefits

- **Enhanced Visitor Experience**: By automating the ticketing process, visitors can enjoy a hassle-free experience, leading to higher satisfaction and increased ticket sales.
- **Operational Efficiency**: Museum staff can focus on more critical tasks as the system reduces manual workload, improving overall operational efficiency.
- **Environmental Sustainability**: The digital ticketing system minimizes the need for printed tickets, contributing to eco-friendly practices.
- **Cultural Promotion**: By making museums more accessible, the platform fosters cultural education and engagement.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NIKHIL0VERMA/Darshan_Doot.git
   cd Darshan_Doot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Ensure you have MySQL installed and running.
   - Create a database and update the `.env` file with your database credentials.

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://localhost:8000/`.
- Use the admin panel at `http://localhost:8000/admin/` to manage users and bookings.

## Configuration

Ensure you have a `.env` file in the root/app directory take a look at `.env.example` file.

## Credits

I would like to acknowledge the contributions of the following team members:

- **Anoop Raj**: Chatbot booking implementation and presentation.
- **Gargi Barman**: Translation of the bot and testing.
- **Piyush**: Botpress integration with WhatsApp and implementation of monitoring features in the backend.
- **Khushi Agrawal**: Data collection to feed the bot.
- **Anubhav Srivastava**: Data sanitization and backend integration with Botpress.


### NOTE
*This project is currently hosted on PythonAnywhere for internal use only within Bootpress.*

*We are building this and waiting for SIH 2024 result*
