public class WhatsApp
{
    public void EnviarMensagem(string numero, TextMessage message){
        Console.WriteLine($"Enviando mensagem de texto para o número {numero}");
    }

    public void EnviarMensagem(string numero, VideoMessage message){
     Console.WriteLine($"Enviando um vídeo para o número {numero}");
    }

     public void EnviarMensagem(string numero, PhotoMessage message){
        Console.WriteLine($"Enviando uma foto para o número {numero}");
    }
     public void EnviarMensagem(string numero, FileMessage message){
        Console.WriteLine($"Enviando um arquivo para o número {numero}");
    }



    
}