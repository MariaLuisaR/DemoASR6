from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Cliente, Oferta
from twilio.rest import Client
from django.shortcuts import redirect




def upload_file(request):
    Cliente.objects.all().delete()
    Cliente.generate_clientes()
    Oferta.objects.all().delete()
    clientes = Cliente.objects.all()
    return render(request, 'index.html', {'clientes': clientes})

def enviar_email(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Cliente.objects.get(pk=cliente_id)

        oferta = Oferta.objects.create(nombre=cliente.nombre)

        last_oferta_id = Oferta.objects.latest('id').id

        cupo_credito = '10,000,000 COP'
        tasa_interes = '18%'
        fecha_corte = '15 de cada mes'
        fecha_pago = 'Último día de cada mes'

        oferta_url = f"http://127.0.0.1:8000/aceptar_oferta/{last_oferta_id}/"

        subject = 'Aprobación tarjeta de crédito'
        message = f"Estimado/a {cliente.nombre},\n\n"
        message += "Nos complace anunciarle que su solicitud de tarjeta de crédito ha sido aprobada para las siguientes características:\n\n"
        message += f"- Cupo de crédito: {cupo_credito}\n"
        message += f"- Tasa de interés: {tasa_interes}\n"
        message += f"- Fecha de corte: {fecha_corte}\n"
        message += f"- Fecha de pago: {fecha_pago}\n\n"
        message += "Para aceptar la oferta de tarjeta de crédito, por favor ingrese al siguiente enlace:\n"
        message += f"{oferta_url}\n\n"
        message += "Por favor, no dude en contactarnos si tiene alguna pregunta o necesita más información.\n\n"
        message += "Atentamente,\nBanco de los Alpes"

        send_mail(subject, message, 'a.serranoc@uniandes.edu.co', [cliente.correo])

        return redirect('correo_enviado')
    else:
        return HttpResponse("Método no permitido.")
def aceptar_oferta(request, pk):
    oferta = Oferta.objects.get(pk=pk)
    if oferta.estado == 'aceptado':
        return render(request, 'oferta_caducada.html')
    oferta.estado = 'aceptado'
    oferta.save()
    cliente = Cliente.objects.get(nombre=oferta.nombre)
    nombre_cliente = cliente.nombre
    telefono_cliente = cliente.telefono
    if not telefono_cliente.startswith('+57'):
        telefono_cliente = '+57' + telefono_cliente
    account_sid = 'AC11ce85e890d998ce6c042db85b25d406'
    auth_token = 'c3540b7c8b8729a1e8b7872ae42baf8e'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        #to=telefono_cliente,
        to='+573044067010',
        from_='+12568260034',
        body=f"Felicitaciones, {nombre_cliente}! Su oferta ha sido aceptada con éxito."
    )
    return render(request, 'aceptar_oferta.html', {'nombre_cliente': nombre_cliente})

def correo_enviado(request):
    return render(request, 'correo_enviado.html')
