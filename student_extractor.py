import streamlit as st
import pdfplumber
import re
import pandas as pd
from fuzzywuzzy import process, fuzz

# Permanent Master List (Embedded from CSV)
master_list = {
    "Arias Tomas ": "5-1",
    "Chokkar Rudransha ": "5-1",
    "Choudhary Rayansh ": "5-1",
    "Benejam Graterol Gabriela De Dios": "5-1",
    "De la Rosa Tomás": "5-1",
    "Duffoo Limay Kiara Paola": "5-1",
    "Duque Lopez Tiago Josue": "5-1",
    "Fajardo Layla ": "5-1",
    "Garces Valeria ": "5-1",
    "Gonzalez Marrugo Sebastian": "5-1",
    "Guerra Paloma ": "5-1",
    "Kishore Aryan ": "5-1",
    "Llanos Landa Emiliana ": "5-1",
    "Moreno Escobar Paulina ": "5-1",
    "Moreno Juan Jose ": "5-1",
    "Munar Isabella ": "5-1",
    "Posada Matias ": "5-1",
    "Ramazanli Abdullah ": "5-1",
    "Ramirez Barrera Isaak ": "5-1",
    "Schwed Andres ": "5-1",
    "Vargas Flórez Valeria ": "5-1",
    "Viteri-Leroux Isabella ": "5-1",
    "Benitez Pablo ": "5-2",
    "Escobar Nicolas ": "5-2",
    "Fernández Violeta ": "5-2",
    "Góngora Bonilla Luciana ": "5-2",
    "Gutierrez Martina ": "5-2",
    "Herrán Bonilla Lucas ": "5-2",
    "Labastida Andrea ": "5-2",
    "Liévano Roncancio Mariana ": "5-2",
    "McKenna Ramirez Liam ": "5-2",
    "Moncada Victoria ": "5-2",
    "Niño Ariza Gabriel": "5-2",
    "Ordoñez Santiago ": "5-2",
    "Paez Muñoz Valeria ": "5-2",
    "Prieto Jacobo ": "5-2",
    "Ramirez Emilio ": "5-2",
    "Reynales Vargas Violeta ": "5-2",
    "Rodriguez Juan Miguel ": "5-2",
    "Romero Luciana ": "5-2",
    "Serpa Sergio ": "5-2",
    "Vargas Ortegon Maria Juliana ": "5-2",
    "Villamil Daniel ": "5-2",
    "Vives Eguis Ignacio ": "5-2",
    "Alvarez Mancina Isabella ": "5-3",
    "Arias Sandoval Martín Pablo ": "5-3",
    "Barreto Agudelo Juan Diego ": "5-3",
    "Bonilla Sarah": "5-3",
    "Castro Santiago ": "5-3",
    "Cubillos Garcia Antonia": "5-3",
    "De Urbina Mariana ": "5-3",
    "Ferreira Valerie ": "5-3",
    "Iriondo Tomas ": "5-3",
    "Martinez Bustillo Simona ": "5-3",
    "Mercado Victoria ": "5-3",
    "Murcia Sebastian ": "5-3",
    "Ochoa Tomas ": "5-3",
    "Ordoñez Nicolas ": "5-3",
    "Ortiz Luciana ": "5-3",
    "Pinzón Barragán Jerónimo ": "5-3",
    "Press Emma ": "5-3",
    "Rico Luciana ": "5-3",
    "Rozo Alejandro ": "5-3",
    "Serrano Ortega Mariana ": "5-3",
    "Tovar Puyana Tomas": "5-3",
    "Urrego Emiliano ": "5-3",
    "Vizcaino David ": "5-3",
    "Arango Rey Lucas ": "5-4",
    "Arbelaez Duque Tomás ": "5-4",
    "Arévalo Cardona Emiliana ": "5-4",
    "Chapman Iglesias Manuela ": "5-4",
    "Ferrer Sofía ": "5-4",
    "Gomez Bonilla Juan Manuel ": "5-4",
    "Heinen Sofía ": "5-4",
    "Hernandez Julieta ": "5-4",
    "Iriondo Miranda ": "5-4",
    "María Juan Andrés ": "5-4",
    "Mora Samuel ": "5-4",
    "Nieto Martina ": "5-4",
    "Niño Rodríguez Jerónimo ": "5-4",
    "Paredes Sebastian ": "5-4",
    "Ranea Doña Juan Ignacio": "5-4",
    "Robayo Sebastian ": "5-4",
    "Rodríguez Peña Esteban ": "5-4",
    "Rojas Emiliano ": "5-4",
    "Rubiano Silvana ": "5-4",
    "Ruiz Mario ": "5-4",
    "Varon Luciana ": "5-4",
    "Atkinson Cruz Lucas": "6-1",
    "Beltran Tamara Jeronimo": "6-1",
    "Camargo Vargas Antonio": "6-1",
    "Cardenas Cardenas Samuel": "6-1",
    "Castellanos Mejía María Paula": "6-1",
    "Chiara Aurelie Marie De Maupeou D´ableiges": "6-1",
    "Daza Torres Eugenia Sofía": "6-1",
    "Kumar Pandey Ayush": "6-1",
    "Maya Salas Juan Camilo": "6-1",
    "Molina Kackson Antonia Joy": "6-1",
    "Montenegro Berrocal Juan Felipe": "6-1",
    "Pedraza Soto Luciana": "6-1",
    "Roa Camacho Manuela": "6-1",
    "Roca Chilson Samuel": "6-1",
    "Stephens Maximo": "6-1",
    "Triviño Huertas Juan Martín": "6-1",
    "Valderrama Gutierrez Santiago": "6-1",
    "Vargas Córdoba Nathalia": "6-1",
    "Yunis Omaña María Antonella": "6-1",
    "Aldana Ocando Juan Eduardo": "6-2",
    "Bernal Franco Nicolas": "6-2",
    "Brasesco González Stefano": "6-2",
    "Caballero Ramírez Gabriela": "6-2",
    "Camacho Orozco Rafael": "6-2",
    "Cruz Jaramillo Santiago": "6-2",
    "Jiménez Ocando Emma": "6-2",
    "Lamprea Delgado Maria Adelaida": "6-2",
    "Martinez Barrera Gabriela": "6-2",
    "Mejía Bernal Joaquín": "6-2",
    "Neira Aristizabal Juan Sebastián": "6-2",
    "Peña Hernandez Jose Alejandro": "6-2",
    "Quintero Montes Lucas": "6-2",
    "Sánchez Castilla Valeria": "6-2",
    "Sanchez Garcia Sofia": "6-2",
    "Urrea Moreno Maria Lucia": "6-2",
    "Valderrama Lenis Julieta": "6-2",
    "Acerbo Cuevas Luca": "6-3",
    "Atkinson Cruz Dylan": "6-3",
    "Barbosa Guerra Emilia": "6-3",
    "Bonilla Silva Manuela": "6-3",
    "Cortez Ladino Maria Fernanda": "6-3",
    "Costilla Cortina Antonio": "6-3",
    "Cuestas Rodriguez Danna Nicole": "6-3",
    "Gomez Nova Andres David": "6-3",
    "Jiménez Basabe Juana": "6-3",
    "Lacouture Elias Juan Pablo": "6-3",
    "María Gaviria Martín ": "6-3",
    "Pardo Sabogal Camila": "6-3",
    "Poveda Bolaños Isabella": "6-3",
    "Rodriguez Verdugo Juan Nicolas": "6-3",
    "Salazar Bayona Juan David": "6-3",
    "Troya More Matias": "6-3",
    "Valderrama Portocarrero Gabriel Fernando": "6-3",
    "Vanegas Zamora Luciana": "6-3",
    "Velandía Aldana Samuel Esteban": "6-3",
    "Aguilar Barón Matías": "6-4",
    "Cárdenas Ramírez Briana Estefanía": "6-4",
    "Castellanos Soledad Alejandro": "6-4",
    "Castro Sánchez Isabella": "6-4",
    "Fernández Enciso Simón": "6-4",
    "Figueredo Fontalvo Alessandro": "6-4",
    "Leiva Perez Jerónimo": "6-4",
    "Lozano Vanegas Isabella": "6-4",
    "Machacón Martinez Gabriela": "6-4",
    "Malo Anzola Matías": "6-4",
    "Molina Bohórquez Santiago": "6-4",
    "Morales Centeno Alejandro": "6-4",
    "Muñoz Parra Alejandra": "6-4",
    "Muñoz Vacca Juan Felipe": "6-4",
    "Nobili Pittilini Clara": "6-4",
    "Nossa Díaz Mariana": "6-4",
    "Oswald Angulo Francisca Alejandra": "6-4",
    "Rojas Montejo Jorge Mauro": "6-4",
    "Sánchez Olmos Antonia": "6-4",
    "Sintura Salazar Jerónimo": "6-4",
    "Suarez Villate Tomas": "6-4",
    "Triviño Piñeros Verónica": "6-4",
    "Alvarez Herrera Daniella Sofia": "6-5",
    "Baez Suarez Sofía": "6-5",
    "Cano Quijano Daniel Steven": "6-5",
    "Cárdenas Gañan Luis Santiago": "6-5",
    "Casadiego Duran Samuel Eduardo": "6-5",
    "Castillo Tovar Tomás Camilo": "6-5",
    "Forero Acero Juanita": "6-5",
    "Giraldo Pachón Danna": "6-5",
    "Guzmán Echeverri Martín": "6-5",
    "Hurtado Borja Esteban": "6-5",
    "Juyar Prieto Emma Sofía": "6-5",
    "Martinez Bernal Salomé": "6-5",
    "Mejía Macias Antonella": "6-5",
    "Molina Lugo Alejandro": "6-5",
    "Pinzón Manrique Sofía": "6-5",
    "Prieto Lozano Martín Andrés": "6-5",
    "Quintero Ortega Antonia": "6-5",
    "Rincón Moreno Matías": "6-5",
    "Rojas Carvajal Emilio": "6-5",
    "Rueda Charry Emilio": "6-5",
    "Vásquez Serrano Juan Felipe": "6-5",
    "Vélez Moreno Paloma": "6-5",
    "Becerra Peralta,  María José": "7-1",
    "Buendia Sepulveda Daniel": "7-1",
    "Contreras Duran Paola Andrea": "7-1",
    "Escobar Diaz Juan Martin ": "7-1",
    "Garcia Huertas Kyra Sophia": "7-1",
    "Garzon Hidalgo Sergio Esteban": "7-1",
    "Gomez Ochoa Lorenzo ": "7-1",
    "Herrera Cufiño Maria Gabriela": "7-1",
    "Lara Laino Jeronimo": "7-1",
    "Pardo Lopez Sara": "7-1",
    "Pedrero Florez Santiago": "7-1",
    "Peñuela Gomez Andres": "7-1",
    "Press Tobon Ilan": "7-1",
    "Quiñones Soler  Martin ": "7-1",
    "Restrepo Tobon  Valentina": "7-1",
    "Rey Ramirez, Matias": "7-1",
    "Rodriguez Rojas Jeronimo": "7-1",
    "Salcedo Brown,  Luna Loraine": "7-1",
    "Sandoval Hernandez Martín": "7-1",
    "Serna Amorocho Valentina": "7-1",
    "Tamayo Salazar, Amelia": "7-1",
    "Umbarila Cabrera Daniel Felipe": "7-1",
    "Wilches Hernandez,  Maria Jose": "7-1",
    "Anaya Omaña,  Luna Sofia": "7-2",
    "Arevalo Gallego Lorenzo": "7-2",
    "Carnevali Mesquita Spranger Manuela": "7-2",
    "Cavinato Ramírez Luca": "7-2",
    "Chacon Gonzalez  Valeria ": "7-2",
    "Cruz Saenz  Anabella ": "7-2",
    "De La Espriella Caliz Manuella": "7-2",
    "Fajardo Alba Sebastián": "7-2",
    "Fuquen Molano  Martin": "7-2",
    "Jiménez Fadul María José": "7-2",
    "López Moreno  Juan Jacobo": "7-2",
    "Olarte Estrada Isabela": "7-2",
    "Payro Lopez, Arturo": "7-2",
    "Pinilla Navia Alicia": "7-2",
    "Prem Nainish Vembu  Aniketa": "7-2",
    "Reales Gamboa Julieta": "7-2",
    "Rincon Suarez Sara Victoria": "7-2",
    "Salcedo Castillo Ana Victoria": "7-2",
    "Sandoval Ruge  Gabriella ": "7-2",
    "Tobias Morales  Jorge Santiago": "7-2",
    "Uribe Guiza Antonia": "7-2",
    "Varela Jimenez  Santiago ": "7-2",
    "Vargas Córdoba Felipe": "7-2",
    "Bayona Herrera  Jacobo ": "7-3",
    "Castellanos Moreno Juan Andrés": "7-3",
    "Certuche Rincon,  Joao Andres": "7-3",
    "Echeverry Durán Samuel": "7-3",
    "Ferrari Cranwell, Diego": "7-3",
    "Jimenez Salamanca Veronica": "7-3",
    "Lozano Martinez David Jeronimo": "7-3",
    "Maldonado Puentes Gabriela": "7-3",
    "Martinez Morales Alejandra": "7-3",
    "Martinez Torres Gabriel Alfredo": "7-3",
    "Marume Benitez Sarah": "7-3",
    "Mendez Ruiz Isabella": "7-3",
    "Mercado Merchán Matías": "7-3",
    "Quintero Ortega Luciana": "7-3",
    "Rubiano Rincon Emilio": "7-3",
    "Sanchez Cortes, Lorenzo": "7-3",
    "Saray Martinez, Mateo": "7-3",
    "Torres Lopez, Juana": "7-3",
    "Valero Pinzon Sebastian": "7-3",
    "Vasco Callejas Samuel": "7-3",
    "Yaya Ladino Isabella": "7-3",
    "Zabala Diaz Emily": "7-3",
    "Arevalo Rojas Manuel Esteban": "7-4",
    "Asseiceiro Ferreira Matias Daniel": "7-4",
    "Ayala Forero Camilo": "7-4",
    "Castillo Tovar Simón": "7-4",
    "Cerball Segura Nina Lucia": "7-4",
    "Cristancho Alzate Lucas": "7-4",
    "Diaz Upegui Sara": "7-4",
    "Góngora Santiago": "7-4",
    "Gutiérrez Santos Emiliano": "7-4",
    "Hernandez Coral Ivana": "7-4",
    "Hernández Eslava Matias": "7-4",
    "Jimenez Fadul Juan Diego": "7-4",
    "Lozano Ardila Silvana": "7-4",
    "Natale Lapelosa Nicolas Carmelo": "7-4",
    "Nieto Gonzalez  Camila ": "7-4",
    "Orozco Cortes Matias": "7-4",
    "Orozco Herrera Maria Gabriela": "7-4",
    "Sanabria Puerta Luciano": "7-4",
    "Sanchez Cabrera  Maria Isabella": "7-4",
    "Saray Martinez Felipe": "7-4",
    "Sealy Rodriguez Aldair Elias ": "7-4",
    "Tobón Marín Sofia": "7-4",
    "Aguilera Hidalgo, Juanita": "7-5",
    "Arellano Varon Martín Andrés": "7-5",
    "Ariza Londoño, Salomé": "7-5",
    "Brasesco González Enzo": "7-5",
    "Bustamente Cabrera Antonio": "7-5",
    "Camacho Forero Ana Sofía ": "7-5",
    "Castro Bornacelli Daniel Felipe": "7-5",
    "Fandiño Peña Samuel": "7-5",
    "Fernandez Enciso  Martin": "7-5",
    "Florez Roman,  Juan Andres": "7-5",
    "Gomez Carpintero Ane": "7-5",
    "Gonzalez Bonilla Manuela": "7-5",
    "Luque García Catalina": "7-5",
    "Mc Kenna Ramirez Samuel Aidan": "7-5",
    "Navarro Cubides Pedro David": "7-5",
    "Ramirez Padilla, Matias": "7-5",
    "Sánchez Olmos Valeria": "7-5",
    "Sengar Riddhi": "7-5",
    "Tobon Pinilla  Juan Andres ": "7-5",
    "Valenzuela  Burbano Alejandro": "7-5",
    "Zarza Carbonell Daniel": "7-5",
    "Alpire Caballero Jazmin Mirtha": "8-1",
    "Bravo Hirsch Nicolas Ignacio": "8-1",
    "Calvache Bustos Nicolás": "8-1",
    "Camacho Orozco Camila": "8-1",
    "Chávez Del Portillo Enrique Javier": "8-1",
    "Clavijo Vergara Camila": "8-1",
    "Echeverri Lozano Laura Alejandra": "8-1",
    "Gualdrón Suárez Manuela": "8-1",
    "Gunda Nirvigna": "8-1",
    "Guzmán Martínez Alejandro": "8-1",
    "Jiménez García Bárbara": "8-1",
    "Liu Yicen": "8-1",
    "Ortiz Hernández María Juliana": "8-1",
    "Pillai Suryanarayanan V": "8-1",
    "Prem Nainish Vembu Anirudha": "8-1",
    "Pulido Tamayo Valeria Mae": "8-1",
    "Serna Saucedo Alejandro": "8-1",
    "Villa Herrera Jerónimo": "8-1",
    "Viteri Leroux Abigail": "8-1",
    "Yepes Polanía Andrés": "8-1",
    "Arias Sandoval Manuela": "8-2",
    "Benítez Navarro Isabella": "8-2",
    "Blanco Ribón Mariana Gabriela": "8-2",
    "Cáceres Moreno Lucía": "8-2",
    "Castro Aranguren Mariana": "8-2",
    "Ferrer Villota Santiago": "8-2",
    "Granada Rincón Antonia": "8-2",
    "Guerra Messier Samuel ": "8-2",
    "Jones Castellanos Simón": "8-2",
    "Leon Guarnizo Valentina": "8-2",
    "López Castrillón Luciana": "8-2",
    "Machacón Martínez Sofía": "8-2",
    "Macías Ceballos Daniel": "8-2",
    "Montoya Sánchez Silvana": "8-2",
    "Moscoso Fajardo Santiago": "8-2",
    "Mosquera Garcia Lucia": "8-2",
    "Padilla Sebastian ": "8-2",
    "Rivera Forero Ana Sofía": "8-2",
    "Rodriguez Estepa Maria Jose ": "8-2",
    "Roldán Umbarila Federico": "8-2",
    "Rozo Lerzundy Antonio": "8-2",
    "Triana González Valerie": "8-2",
    "Valbuena Díaz Gabriela": "8-2",
    "Vargas Ortegón Samuel": "8-2",
    "Arango Rey Sofía": "8-3",
    "Ballesteros Ulloa Martín": "8-3",
    "Becerra Maya Valeria": "8-3",
    "Benitez Santiago ": "8-3",
    "Castillo Jaar Maria Paula ": "8-3",
    "Echeverri Lozano Luciana": "8-3",
    "Escobar Espinosa Santiago": "8-3",
    "Giraldo Pachon Salome": "8-3",
    "Gualdrón Bocanegra Paula Mariana": "8-3",
    "Iriondo Cortés Simón": "8-3",
    "Ladino Castilla Rebecca": "8-3",
    "Mesa Blanco Juan Lucas": "8-3",
    "Morales Ospina Samuel": "8-3",
    "Orjuela Henao Matías ": "8-3",
    "Peña Araque Nicolás": "8-3",
    "Pinzón Casas Manuel Alejandro": "8-3",
    "Prieto Montenegro Gabriela": "8-3",
    "Romay Torres Andrés Ignacio": "8-3",
    "Sarmiento Guzmán Mariana": "8-3",
    "Triviño Piñeros Manuela ": "8-3",
    "Vásquez Serrano Nicolás José": "8-3",
    "Villamil Bermúdez Sara Lucía": "8-3",
    "Valero Mario ": "8-3",
    "Acevedo Ramírez Juan Sebastián": "8-4",
    "Ardila Mateus Juliana": "8-4",
    "Bedoya Delgadillo María Paz": "8-4",
    "Bravo Hirsch Fernando Arturo": "8-4",
    "Camacho Daza Mariana": "8-4",
    "Cormane López Isabella": "8-4",
    "De Castro Uribe Sara": "8-4",
    "Díaz Hernández Cesar Andrés": "8-4",
    "González Del Gordo Santiago": "8-4",
    "Herrera Alvarado Sofía Montserrat": "8-4",
    "Herrera Castro Manuela": "8-4",
    "Herrera Gómez Nicolás": "8-4",
    "Ladino Chiquillo Silvana": "8-4",
    "Loaiza Rua Martín": "8-4",
    "Martinez Pinto Daniela ": "8-4",
    "Morales Cuellar Maria José": "8-4",
    "Ramos Eslava Santiago": "8-4",
    "Rojas Silva Santiago": "8-4",
    "Serna Amorocho Mariana": "8-4",
    "Soler Castro Sebastián": "8-4",
    "Uribe Juan Diego ": "8-4",
    "Borras Valero Mariana": "8-4",
    "Berrocal Agudelo Juan Felipe": "8-5",
    "Casas Cortes Sofia": "8-5",
    "Herrera Sánchez María Paula": "8-5",
    "Kiger De La Rosa Sophia": "8-5",
    "Ladino Chiquillo Fernanda": "8-5",
    "Lizarazo Naomi": "8-5",
    "Lopez Gutierrez Mariana": "8-5",
    "Martínez Giraldo Taliana": "8-5",
    "Molina Reyes Daniel": "8-5",
    "Monroy Romero Gabriel ": "8-5",
    "Morales Cárdenas Isabella": "8-5",
    "Perez Arbelaez Juan Felipe": "8-5",
    "Perez Becerra Catalina": "8-5",
    "Pinilla Salamanca Santiago": "8-5",
    "Ríos Tamayo Manuela": "8-5",
    "Romero López Alicia": "8-5",
    "Rozo Téllez Juan Sebastián": "8-5",
    "Vargas Cerón Luana": "8-5",
    "Baene Senior Santiago": "9-1",
    "Bohórquez Bermúdez Nicolás": "9-1",
    "Díaz Garrido Daniel": "9-1",
    "Domínguez Cristiani Valeria": "9-1",
    "Duque Daza Valeria": "9-1",
    "Flórez Román Miguel José": "9-1",
    "Gómez Nova Karen Sofía": "9-1",
    "Lizarazo Mateo": "9-1",
    "López Riascos María Paz": "9-1",
    "López Rodríguez Santiago": "9-1",
    "Martínez Pinto Juliana Sofía": "9-1",
    "Martinez Tellez Juan Jose": "9-1",
    "Mendoza Herrera Esteban": "9-1",
    "Muñoz Parra Catalina": "9-1",
    "Orozco Cortés Jerónimo": "9-1",
    "Ospina Sanchez Emiliana": "9-1",
    "Parias Gomez Sofia": "9-1",
    "Sarmiento Rivera Gabriela": "9-1",
    "Serrano Roca Camilo": "9-1",
    "Tovar Varcacel Juan Pablo": "9-1",
    "Vergel De León Sebastián": "9-1",
    "Amézquita Arciniegas Luciana": "9-2",
    "Buenaventura Chianca Joaquín Arthur": "9-2",
    "Cabrera Franco Jacobo": "9-2",
    "Calvete Soto Sofía": "9-2",
    "Cárdenas Orjuela Isabella": "9-2",
    "Gómez Ochoa Renata": "9-2",
    "Herrera Rojas Martín": "9-2",
    "Jiménez Román Paloma": "9-2",
    "Londoño Bernaza Lucas": "9-2",
    "Madeira De Castro Davi": "9-2",
    "Mc Kenna Ramírez John Michael": "9-2",
    "Melchior Gilles Charles Marie": "9-2",
    "Prajit Naik": "9-2",
    "Ramírez Pacheco Kenny Alejandro": "9-2",
    "Rey Ortiz Sara Valentina": "9-2",
    "Rojas Reinoso Juan Jacobo": "9-2",
    "Roldán Cortés David": "9-2",
    "Rossi Garcia Renato": "9-2",
    "Vallejo Castañeda Luciano": "9-2",
    "Wilches Jaramillo David Eduardo": "9-2",
    "Alvarez Herrera David Alejandro": "9-3",
    "Ardila Rivera María Alejandra": "9-3",
    "Arias Zapata Ana María": "9-3",
    "Barcenas Nicolas": "9-3",
    "Bernal Rodríguez Juan Felipe": "9-3",
    "Cardona Mantilla Ángel": "9-3",
    "Cruz Sáenz Brianna María": "9-3",
    "Cuellar Moreno Fátima Lucciana": "9-3",
    "Gaitán Gómez Felipe": "9-3",
    "García Barona Susana": "9-3",
    "González Galvis Juan Pablo": "9-3",
    "López Serna Lorenzo": "9-3",
    "Niño Pinto Lorenzo": "9-3",
    "Obando Pérez Laura": "9-3",
    "Patiño Puerta Juan Felipe": "9-3",
    "Real Manrique Ebalo Simón": "9-3",
    "Rincón Trujillo Mariana": "9-3",
    "Zarza Carbonell Mónica": "9-3",
    "Barbosa Guerra Gabriela": "9-4",
    "Barón Castaño Luna": "9-4",
    "Calle Cuevas Emiliano": "9-4",
    "Calle Ruiz Martina": "9-4",
    "Cárdenas Orjuela Paulina": "9-4",
    "Cortés López Miguel Matías": "9-4",
    "Giraldo Taborda Isabella": "9-4",
    "Gómez Bonilla Eduardo José": "9-4",
    "González Ávila Sofía": "9-4",
    "Herrera Rojas Felipe": "9-4",
    "Jaramillo Buitrago Valentina": "9-4",
    "Munevar Reyes Manuela": "9-4",
    "Pinzón Barragán Sebastián": "9-4",
    "Pinzón Manrique Silvana": "9-4",
    "Prada Torres Silvana": "9-4",
    "Prada Valencia Alejandro": "9-4",
    "Sánchez Escobar Andrés": "9-4",
    "Tavera Cotes Sofía": "9-4",
    "Varela Jiménez Nicolás": "9-4",
    "Zournadjian Maria": "9-4",
    "Arellano Varón Nicolás Alejandro": "9-5",
    "Árevalo Cardona Luciana": "9-5",
    "Balser David Matías": "9-5",
    "Betancur Morales Samuel": "9-5",
    "Capasso Rey Florencia": "9-5",
    "Castellanos Mejía María José": "9-5",
    "Daza Torres Alfonso Ignasio": "9-5",
    "Duque Paredes Santiago": "9-5",
    "Espitia Santamaría Martín": "9-5",
    "García Gómez Jacobo": "9-5",
    "Gómez Sánchez Sofía": "9-5",
    "Millán Cuesta David Alejandro": "9-5",
    "Moncaleano Garavito Paula Jimena": "9-5",
    "Pérez Quintero Martín": "9-5",
    "Ramírez Rojas Mariana": "9-5",
    "Rojas Marulanda Samuel Leonardo": "9-5",
    "Salazar Bayona Laura Juliana": "9-5",
    "Segura Medina Jeronimo ": "9-5",
    "Solano Jiménez Mateo": "9-5",
    "Van-Strahlen Muriel José Pablo": "9-5",
    "Cáceres Moreno Sofía": "10-1",
    "Cárdenas Gañan Sara Valentina": "10-1",
    "Díaz Upegui Sebastián": "10-1",
    "Duque Calixto Juan Antonio": "10-1",
    "Escobar Díaz Gabriela": "10-1",
    "Eslava Eslava Samuel": "10-1",
    "Espinosa Ruiz Maria Alejandra": "10-1",
    "Franco Chacón Juliana María": "10-1",
    "Franco Peralta Susana": "10-1",
    "Guevara Martinez Miguel Angel ": "10-1",
    "Jiménez García María Antonia": "10-1",
    "Lopez Garcia Juan Jose": "10-1",
    "María Gaviria Samuel": "10-1",
    "Sanchez Ospina Gabriela": "10-1",
    "Sarmiento Otero Luciana": "10-1",
    "Solorzano Pineda Valeria  ": "10-1",
    "Tapias Rojas Ana Sofía": "10-1",
    "Uribe Guiza Lorenzo": "10-1",
    "Vargas Martinez Alejandro ": "10-1",
    "Zabala Diaz Isabella ": "10-1",
    "Zarza Carbonell Jaume": "10-1",
    "Alvarez García Gabriela": "10-2",
    "Amaya Gómez Mariana": "10-2",
    "Balser David Samuel": "10-2",
    "Ceron Rincon Mariana": "10-2",
    "Escobar Bernhard Ana María": "10-2",
    "Fúquen Zarabanda Jerónimo": "10-2",
    "Guzman Echeverri Emilio": "10-2",
    "Josephsen Chávez Samuel": "10-2",
    "Juyar Prieto Cira Isabella ": "10-2",
    "Luque García Federico": "10-2",
    "Mesa González Juan Alejandro": "10-2",
    "Otalora González Alejandra": "10-2",
    "Pertuz Schutt Mariana ": "10-2",
    "Pombo Cediel Sofia": "10-2",
    "Rodríguez Verdugo Santiago": "10-2",
    "Rosero Castaño Gabriel": "10-2",
    "Salgado Vélez Mateo": "10-2",
    "Sarmiento Bogotá Luciana ": "10-2",
    "Sierra Tarazona Paula Alejandra": "10-2",
    "Torres Gordillo Juan Andres": "10-2",
    "Umbarila Cabrera Valeria": "10-2",
    "Vargas Vidal Owen": "10-2",
    "Adaime Ochoa Manuela": "10-3",
    "Bastidas Medina Camilo Alejandro": "10-3",
    "Caycedo León Pablo Andrés": "10-3",
    "Correa Giraldo Gabriela": "10-3",
    "De La Espriella Cáliz Salvatore ": "10-3",
    "Domínguez Cristiani Samuel": "10-3",
    "Eslava Obando Sofía": "10-3",
    "Espinosa Balaguera Martín": "10-3",
    "Garzón Ríos Tomás": "10-3",
    "Guevara Rodríguez Mateo": "10-3",
    "Higuera Palacios Nicolás": "10-3",
    "Lozano Ardila Mariana": "10-3",
    "Molina Bohórquez Mariana": "10-3",
    "Molina Lugo Valeria": "10-3",
    "Muriel Caicedo Miranda": "10-3",
    "Ortiz Bonett Emilia": "10-3",
    "Ortiz Roesel Daniel ": "10-3",
    "Pabón Gómez Victoria": "10-3",
    "Rojas Silva Juanita": "10-3",
    "Salazar Gaviria Samuel": "10-3",
    "Tamayo Salazar Tomás": "10-3",
    "Tovar Cortes Samuel ": "10-3",
    "Valencia Bonilla Valentina": "10-3",
    "Andrade Juanita ": "10-4",
    "Bohorquez Villamil Catalina": "10-4",
    "Borras Rey Juan Camilo ": "10-4",
    "Camacho Castrillon Federico": "10-4",
    "Castillo Bastidas Tatiana": "10-4",
    "Ferrer Villota Sara": "10-4",
    "Lopez Moreno Samuel Alejandro ": "10-4",
    "Ortega Diaz Luna": "10-4",
    "Páez Hoyos Valeria": "10-4",
    "Pérez Castro Juan José": "10-4",
    "Pinilla Ramirez Juan Esteban": "10-4",
    "Poveda Bolaños Juan Sebastian": "10-4",
    "Quintero Franco Simón": "10-4",
    "Ramírez Barrera Isabella ": "10-4",
    "Ramos Cáceres Isabela": "10-4",
    "Rebolledo Kerguelen Nicolás": "10-4",
    "Sanchez Tovar Ivanna": "10-4",
    "Shambo Martínez Annie": "10-4",
    "Sophia Valentina Spiliopulos Marfisi": "10-4",
    "Vanstrahlen Durán Alejandra": "10-4",
    "Villamizar Bustamante Gabriel Andrés": "10-4",
    "Capasso Rey Facundo Daniel": "11-1",
    "De La Cruz Galvis María Del Pilar": "11-1",
    "Ferro León Valeria": "11-1",
    "Forero Escobar Nicolás": "11-1",
    "Giraldo Rivas Camila Isabella": "11-1",
    "Gravini Rodríguez Amaranta Carolina": "11-1",
    "Ladino Muñoz Carlos Darío": "11-1",
    "Loaiza Niño Juan David": "11-1",
    "Mejia Navas Sara Luna": "11-1",
    "Millán Cuesta Andrés Felipe": "11-1",
    "Nishizawa Duque Saya Valentina": "11-1",
    "Obando Pérez Emilio": "11-1",
    "Rojas Vargas María Paula": "11-1",
    "Sanchez Ospino Maximiliano ": "11-1",
    "Seth Soham Vishal": "11-1",
    "Silva Mendoza Camila Del Mar": "11-1",
    "Tovar Urdinola Laura Patricia": "11-1",
    "Alarcón Cepeda Ricardo ": "11-2",
    "Benejam Graterol Bárbara": "11-2",
    "Bento Ramos Mariana Isabella": "11-2",
    "Carvajal Polo Samuel ": "11-2",
    "Casado De Lamadrid Paloma": "11-2",
    "Chica Muñoz Lorenzo ": "11-2",
    "Díaz Arias Samuel Esteban": "11-2",
    "Donoso De Lima Marianna": "11-2",
    "López García Juliana": "11-2",
    "Martín Cadavid Samuel": "11-2",
    "Moreno Patiño Daniela": "11-2",
    "Murillo Hincapié Samuel": "11-2",
    "Natale Lapelosa Fabrizio": "11-2",
    "Perez Becerra Maria Alejandra": "11-2",
    "Price Betancourt Daniella María": "11-2",
    "Quintana Gámez Camilo Alejandro": "11-2",
    "Serna Amorocho Alejandro": "11-2",
    "Sorzano Saker Manuela": "11-2",
    "Wilches Hernández Juan Andrés": "11-2",
    "Yamín Delgado Santiago": "11-2",
    "Alzate Gómez Valentina": "11-3",
    "Beltrán Ramírez Juan Esteban": "11-3",
    "Benítez Navarro Daniel Andrés": "11-3",
    "Berrocal Agudelo Leonardo": "11-3",
    "Calle Ruiz Emiliana": "11-3",
    "Escobar Cervantes Juanita": "11-3",
    "Gallo García David Felipe": "11-3",
    "Granada Rincón Valeria": "11-3",
    "Lacouture Elías Mariana": "11-3",
    "López Murillo Alejandro": "11-3",
    "Molina Reyes Ana Sofía": "11-3",
    "Monzón Parada Sofía Alejandra": "11-3",
    "Pérez Quintero Samuel": "11-3",
    "Prieto Rodríguez Juan Andrés": "11-3",
    "Rozo Lerzundy Sofía": "11-3",
    "Sandoval Ramírez Samuel": "11-3",
    "Scavrone Da Cruz Bonato Valentina": "11-3",
    "Soto Rodríguez Juan Pablo": "11-3",
    "Valenzuela Burbano Felipe": "11-3",
    "Zournadjian Sofia": "11-3",
    "Bossa Jattin Zulema María": "11-4",
    "Castillo Muñoz Sara ": "11-4",
    "Diaz Mendez Andrés": "11-4",
    "Duerr Roa Emily Andrea": "11-4",
    "Ferrari Cranwell Clara": "11-4",
    "García Córdoba Miguel Santiago": "11-4",
    "García Montoya Mariana": "11-4",
    "Herrera Gómez Mariana": "11-4",
    "Janssen Villegas Pietro Roberto": "11-4",
    "Jiménez Barbosa Ana Sofía": "11-4",
    "Manrique Cárdenas Nicolás": "11-4",
    "Ortiz Olarte Miguel Ángel": "11-4",
    "Rattner Prieto Monique ": "11-4",
    "Reyna Rincón Sara Sofía": "11-4",
    "Rodríguez Moreno Sofía": "11-4",
    "Sánchez Bonilla Juan José": "11-4",
    "Sánchez Tovar Ilona": "11-4",
    "Silva Mendoza Isabel Sofía": "11-4",
    "Suárez Castro Alejandra": "11-4",
    "Villalba Velandia Isabella Panambi": "11-4",
    "Aguirre Caiza Paula": "11-5",
    "Aguirre Forero Nicolás": "11-5",
    "Fajardo Alba Nicolás": "11-5",
    "Fefer Rodríguez Yael": "11-5",
    "Goldsztayn Bernal Sarah": "11-5",
    "González Upegui Felipe": "11-5",
    "Izquierdo Ortega Felipe": "11-5",
    "Kiger de la Rosa Natalia": "11-5",
    "León Guarnizo Gabriela ": "11-5",
    "Leonel Picker Violeta": "11-5",
    "Maya Salas Mariana": "11-5",
    "Páez Sorzano Sofía": "11-5",
    "Rozo Téllez Ana Camila": "11-5",
    "Rueda Charry Tomás": "11-5",
    "Serrano Roca Valeria": "11-5",
    "Vargas Arias Valentina": "11-5",
    "Vecino Barranco Juan Diego": "11-5",
    "Vergel De León Marianna": "11-5",
    "Wattamwar Tejas Raman": "11-5",
}

# Define valid grades
valid_grades = ["QUINTO", "SEXTO", "SEPTIMO", "OCTAVO", "NOVENO", "DECIMO", "ONCE"]

# Function to normalize names
def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^a-záéíóúñ ]', '', name)
    return name

# Function to split name into components
def split_name_parts(name):
    return set(normalize_name(name).split())

# Function to extract student names and grades from text
def extract_students_info(text):
    pattern = r"Pasajero:\s([A-ZÁÉÍÓÚÑ ]+)\sCurso:\s([A-ZÁÉÍÓÚÑ]+)"
    matches = re.findall(pattern, text)
    students_info = [(match[0].strip(), match[1].strip()) for match in matches]
    return students_info

# Function to find the best match in the master list
def find_best_match(name, grade):
    pdf_name_parts = split_name_parts(name)
    best_match = None
    highest_score = 0

    for master_name in master_list.keys():
        master_name_parts = split_name_parts(master_name)
        common_parts = pdf_name_parts.intersection(master_name_parts)
        score = len(common_parts) / max(len(pdf_name_parts), len(master_name_parts)) * 100

        # Use fuzzy matching as a fallback
        fuzzy_score = fuzz.token_sort_ratio(name, master_name)
        final_score = max(score, fuzzy_score)

        if final_score > highest_score:
            highest_score = final_score
            best_match = master_name

    assigned_class = master_list.get(best_match, "Not Found") if highest_score > 40 else "Not Found"

    # Final check: Grade-Level Consistency
    if assigned_class != "Not Found" and assigned_class.split('-')[0] != str(valid_grades.index(grade) + 5):
        possible_matches = [key for key in master_list.keys() if master_list[key].startswith(str(valid_grades.index(grade) + 5) + '-')]
        best_match, score = process.extractOne(name, possible_matches, scorer=fuzz.token_sort_ratio)
        assigned_class = master_list.get(best_match, "Not Found") if score > 40 else "Not Found"

    return assigned_class

# Streamlit UI
st.title("Student List Extractor")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    students_list = extract_students_info(full_text)
    df = pd.DataFrame(students_list, columns=["Name", "Grade"])
    df = df[df["Grade"].isin(valid_grades)].drop_duplicates()

    progress_bar = st.progress(0)
    total_students = len(df)

    for i, row in df.iterrows():
        df.at[i, "Class"] = find_best_match(row["Name"], row["Grade"])
        progress_bar.progress((i + 1) / total_students)

    # ✅ Fix: Ensure "Class" column exists before sorting
    if "Class" in df.columns and not df["Class"].isnull().all():
        df["Sort_Class"] = df["Class"].apply(lambda x: (int(x.split('-')[0]), int(x.split('-')[1])) if isinstance(x, str) and '-' in x else (99, 99))
        df.sort_values(by=["Sort_Class", "Name"], ascending=[True, True], inplace=True)
        df.drop(columns=["Sort_Class"], inplace=True)

    st.dataframe(df)

    if st.button("Copy to Clipboard"):
        df.to_clipboard(index=False, header=False)
        st.success("Copied to clipboard!")
