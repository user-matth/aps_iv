# APS IV

[<kbd> <br> VER RODANDO <br> </kbd>](http://89.117.51.51:8000/)
[<kbd> <br> VER RODANDO (com domínio) <br> </kbd>](https://unip.cloud/)

The Django Satellite Data Storage and Queue Management Project is a comprehensive Django web application designed to efficiently store satellite data in a database. 

It offers users the ability to organize and manage this data using various data structures, including queues, stacks, trees, and lists. 

![Project Preview](https://user-images.githubusercontent.com/92444207/276792499-d82a2c6f-2e92-4705-8025-3452d1edd4fb.png)

The primary objective of this project is to serve as a minimalistic Django project template that is readily accessible to all users, requiring minimal setup while providing the essential features needed for managing satellite data effectively.

Project is written with django 4.2.6 and python 3.10.11 in mind.
# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com:user-matth/aps_iv.git && cd ./aps_iv

If your project is already cloned first install django by running

    $ pip install django

Get the main dependencies used on the project

    $ pip install faker && pip install pillow && pip install requests && pip freeze > requirements.txt

Then simply apply the migrations:

    $ python3 manage.py makemigrations && python3 manage.py migrate
    
You can now run the development server:

    $ python3 manage.py runserver

### Project features

* Satellite Data Storage: The project is equipped with a robust database system that can store satellite data, ensuring data integrity and availability.
* Queue Management: Users can utilize the queue feature to organize satellite data in a first-in, first-out (FIFO) manner, enabling efficient data processing.
* Stack Management: The stack feature allows users to maintain a last-in, first-out (LIFO) order for satellite data, ensuring flexibility in data handling.
* Tree Structure: Users can create and manage data structures in a tree format, providing a hierarchical view of satellite data for improved organization and navigation.
* List Management: The project includes a list management feature for users to maintain data in a structured list format, allowing for quick access and retrieval.
* Django 4.2.6 Compatibility: Developed using Django 4.2.6, ensuring the latest features and security updates are incorporated into the project.
* Python 3.10.11 Compatibility: The project is built with Python 3.10.11, offering the benefits of the latest Python language enhancements and optimizations.

## Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/92444207?v=4" width="100px;" alt="Foto do Matheus Cardoso Silva no GitHub"/><br>
        <sub>
          <b>Matheus Cardoso Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/103125603?v=4" width="100px;" alt="Foto do Mark Zuckerberg"/><br>
        <sub>
          <b>Matheus Segati Rodrigues</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://i.ibb.co/NYtX18k/Whats-App-Image-2023-10-19-at-11-18-13-PM.jpg" width="100px;" alt="Foto do Steve Jobs"/><br>
        <sub>
          <b>Carolliny Conceição Ribeiro</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

<br><br>
<hr>
<h4 style="text-align:center;">© Copyright, Todos os direitos reservados <a href="https://www.unip.br/" target="_blank">UNIP</a></h4>
