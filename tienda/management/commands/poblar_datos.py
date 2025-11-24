from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de ejemplo'

    def handle(self, *args, **kwargs):
        
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        
        self.stdout.write('Creando categorías...')
        
        cat1 = Categoria.objects.create(
            nombre='Novelas y Ficción',
            descripcion='Libros de narrativa, ciencia ficción, fantasía',
            activo=True
        )
        
        cat2 = Categoria.objects.create(
            nombre='Manga y Cómics',
            descripcion='Manga japonés, manhwa, cómics occidentales',
            activo=True
        )
        
        cat3 = Categoria.objects.create(
            nombre='Libros Técnicos',
            descripcion='Programación, ciencia, tecnología',
            activo=True
        )
        
        cat4 = Categoria.objects.create(
            nombre='Libros Infantiles',
            descripcion='Cuentos, educativos para niños',
            activo=True
        )
        
        cat5 = Categoria.objects.create(
            nombre='Autoayuda y Desarrollo',
            descripcion='Motivación, productividad, psicología',
            activo=True
        )
        
        self.stdout.write('Creando productos...')
        
        productos = [
            {'categoria': cat1, 'nombre': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'editorial': 'Sudamericana', 'isbn': '9788497592208', 'descripcion': 'La obra maestra del realismo mágico que narra la historia de la familia Buendía en el pueblo ficticio de Macondo.', 'precio': Decimal('45.00'), 'precio_descuento': Decimal('35.00'), 'stock': 15, 'destacado': True, 'nuevo': False},
            {'categoria': cat1, 'nombre': '1984', 'autor': 'George Orwell', 'editorial': 'Debolsillo', 'isbn': '9788499890944', 'descripcion': 'Una novela distópica que presenta un futuro totalitario donde el Gran Hermano todo lo ve.', 'precio': Decimal('38.00'), 'stock': 20, 'destacado': True, 'nuevo': False},
            {'categoria': cat1, 'nombre': 'El Principito', 'autor': 'Antoine de Saint-Exupéry', 'editorial': 'Salamandra', 'isbn': '9788498381498', 'descripcion': 'Un cuento poético sobre la amistad, el amor y la pérdida, narrado por un piloto varado en el desierto.', 'precio': Decimal('28.00'), 'precio_descuento': Decimal('22.00'), 'stock': 25, 'destacado': False, 'nuevo': True},
            {'categoria': cat1, 'nombre': 'Harry Potter y la Piedra Filosofal', 'autor': 'J.K. Rowling', 'editorial': 'Salamandra', 'isbn': '9788498382662', 'descripcion': 'El primer libro de la saga que narra las aventuras de Harry Potter en Hogwarts.', 'precio': Decimal('52.00'), 'stock': 18, 'destacado': False, 'nuevo': False},
            
            {'categoria': cat2, 'nombre': 'One Piece Vol. 1', 'autor': 'Eiichiro Oda', 'editorial': 'Ivrea', 'isbn': '9789875622845', 'descripcion': 'El inicio de la aventura de Monkey D. Luffy en busca del tesoro One Piece.', 'precio': Decimal('25.00'), 'precio_descuento': Decimal('20.00'), 'stock': 30, 'destacado': True, 'nuevo': False},
            {'categoria': cat2, 'nombre': 'Naruto Vol. 1', 'autor': 'Masashi Kishimoto', 'editorial': 'Panini', 'isbn': '9788415480013', 'descripcion': 'La historia de Naruto Uzumaki, un ninja adolescente que busca reconocimiento.', 'precio': Decimal('25.00'), 'stock': 28, 'destacado': False, 'nuevo': False},
            {'categoria': cat2, 'nombre': 'Dragon Ball Vol. 1', 'autor': 'Akira Toriyama', 'editorial': 'Planeta', 'isbn': '9788468471563', 'descripcion': 'El comienzo de la aventura de Goku en busca de las esferas del dragón.', 'precio': Decimal('22.00'), 'stock': 35, 'destacado': False, 'nuevo': True},
            {'categoria': cat2, 'nombre': 'Death Note Vol. 1', 'autor': 'Tsugumi Ohba', 'editorial': 'Norma', 'isbn': '9788467904246', 'descripcion': 'Un cuaderno que mata a quien tenga su nombre escrito cae en manos de un estudiante.', 'precio': Decimal('28.00'), 'precio_descuento': Decimal('24.00'), 'stock': 22, 'destacado': True, 'nuevo': False},
            
            {'categoria': cat3, 'nombre': 'Python Crash Course', 'autor': 'Eric Matthes', 'editorial': 'No Starch Press', 'isbn': '9781593279288', 'descripcion': 'Una introducción práctica a la programación en Python para principiantes.', 'precio': Decimal('65.00'), 'stock': 12, 'destacado': False, 'nuevo': True},
            {'categoria': cat3, 'nombre': 'Clean Code', 'autor': 'Robert C. Martin', 'editorial': 'Prentice Hall', 'isbn': '9780132350884', 'descripcion': 'Manual sobre cómo escribir código limpio y mantenible.', 'precio': Decimal('75.00'), 'precio_descuento': Decimal('60.00'), 'stock': 10, 'destacado': True, 'nuevo': False},
            {'categoria': cat3, 'nombre': 'Introducción a los Algoritmos', 'autor': 'Thomas H. Cormen', 'editorial': 'MIT Press', 'isbn': '9780262033848', 'descripcion': 'El libro definitivo sobre algoritmos y estructuras de datos.', 'precio': Decimal('95.00'), 'stock': 8, 'destacado': False, 'nuevo': False},
            {'categoria': cat3, 'nombre': 'JavaScript: The Good Parts', 'autor': 'Douglas Crockford', 'editorial': "O'Reilly", 'isbn': '9780596517748', 'descripcion': 'Una guía para entender las mejores características de JavaScript.', 'precio': Decimal('58.00'), 'stock': 15, 'destacado': False, 'nuevo': False},
            
            {'categoria': cat4, 'nombre': 'El Grúfalo', 'autor': 'Julia Donaldson', 'editorial': 'Macmillan', 'isbn': '9788479717643', 'descripcion': 'Un ratoncito se inventa un monstruo para asustar a sus depredadores.', 'precio': Decimal('32.00'), 'precio_descuento': Decimal('28.00'), 'stock': 20, 'destacado': False, 'nuevo': True},
            {'categoria': cat4, 'nombre': 'Donde viven los monstruos', 'autor': 'Maurice Sendak', 'editorial': 'Kalandraka', 'isbn': '9788484641056', 'descripcion': 'Max viaja a una isla donde viven los monstruos y se convierte en su rey.', 'precio': Decimal('35.00'), 'stock': 18, 'destacado': True, 'nuevo': False},
            {'categoria': cat4, 'nombre': 'El Principito (Edición Infantil)', 'autor': 'Antoine de Saint-Exupéry', 'editorial': 'Salamandra', 'isbn': '9788498386561', 'descripcion': 'Versión ilustrada para niños del clásico de Saint-Exupéry.', 'precio': Decimal('38.00'), 'stock': 25, 'destacado': False, 'nuevo': False},
            {'categoria': cat4, 'nombre': 'La Oruga Muy Hambrienta', 'autor': 'Eric Carle', 'editorial': 'Kókinos', 'isbn': '9788496629080', 'descripcion': 'Una oruga come de todo hasta convertirse en una hermosa mariposa.', 'precio': Decimal('28.00'), 'precio_descuento': Decimal('22.00'), 'stock': 30, 'destacado': False, 'nuevo': False},
            
            {'categoria': cat5, 'nombre': 'Hábitos Atómicos', 'autor': 'James Clear', 'editorial': 'Diana', 'isbn': '9786070756566', 'descripcion': 'Cómo los pequeños cambios generan resultados extraordinarios.', 'precio': Decimal('48.00'), 'precio_descuento': Decimal('40.00'), 'stock': 22, 'destacado': True, 'nuevo': True},
            {'categoria': cat5, 'nombre': 'El Poder del Ahora', 'autor': 'Eckhart Tolle', 'editorial': 'Gaia', 'isbn': '9788484454014', 'descripcion': 'Una guía para la iluminación espiritual viviendo en el presente.', 'precio': Decimal('42.00'), 'stock': 18, 'destacado': False, 'nuevo': False},
            {'categoria': cat5, 'nombre': 'Padre Rico, Padre Pobre', 'autor': 'Robert Kiyosaki', 'editorial': 'Aguilar', 'isbn': '9786073117623', 'descripcion': 'Lecciones sobre finanzas personales e inversión.', 'precio': Decimal('45.00'), 'stock': 20, 'destacado': True, 'nuevo': False},
            {'categoria': cat5, 'nombre': 'Los 7 Hábitos de la Gente Altamente Efectiva', 'autor': 'Stephen Covey', 'editorial': 'Paidós', 'isbn': '9788449334955', 'descripcion': 'Principios fundamentales para el desarrollo personal y profesional.', 'precio': Decimal('52.00'), 'precio_descuento': Decimal('45.00'), 'stock': 16, 'destacado': False, 'nuevo': False},
        ]
        
        for prod_data in productos:
            Producto.objects.create(**prod_data)
        
        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(productos)} productos en {Categoria.objects.count()} categorías'))