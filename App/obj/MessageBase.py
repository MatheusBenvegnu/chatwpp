from datetime import datetime
from abc import ABC, abstractmethod

class MessageBase(ABC):
    """
    Classe base abstrata para todos os tipos de mensagens.
    Define a estrutura comum e o método abstrato de envio.
    """
    def __init__(self, message: str, file_path: str = None, file_format: str = None):
        self._message = message
        self._file_path = file_path
        self._file_format = file_format
        self._send_date = datetime.now()

    # Encapsulamento: Propriedades de leitura
    @property
    def message(self) -> str:
        return self._message

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def file_format(self) -> str:
        return self._file_format

    @property
    def send_date(self) -> datetime:
        return self._send_date

    @abstractmethod
    def get_details(self) -> dict:
        """Retorna um dicionário com os detalhes específicos da mensagem."""
        return {
            "mensagem": self._message,
            "data_envio": self._send_date.strftime("%Y-%m-%d %H:%M:%S"),
            "caminho_arquivo": self._file_path,
            "formato_arquivo": self._file_format
        }

    @abstractmethod
    def send(self, channel: 'ChannelBase', recipient: str):
        """
        Método abstrato para envio da mensagem.
        Polimorfismo será aplicado nas classes filhas.
        """
        pass

class TextMessage(MessageBase):
    """Mensagem simples de texto."""
    def __init__(self, message: str):
        # Herança: Chama o construtor da classe base
        super().__init__(message)

    def get_details(self) -> dict:
        # Polimorfismo: Sobrescreve o método para retornar apenas detalhes de texto
        base_details = super().get_details()
        return {
            "tipo": "Texto",
            "mensagem": base_details["mensagem"],
            "data_envio": base_details["data_envio"]
        }

    def send(self, channel: 'ChannelBase', recipient: str):
        # Polimorfismo: Implementação específica de envio de texto
        channel.send_text(self, recipient)

class MediaMessage(MessageBase, ABC):
    """Classe base abstrata para mensagens com mídia (Foto, Vídeo, Arquivo)."""
    def __init__(self, message: str, file_path: str, file_format: str):
        # Encapsulamento: Validação de dados
        if not file_path or not file_format:
            raise ValueError("Caminho e formato do arquivo são obrigatórios para mensagens de mídia.")
        super().__init__(message, file_path, file_format)

    def get_details(self) -> dict:
        # Herança: Adiciona detalhes de arquivo aos detalhes base
        base_details = super().get_details()
        return {
            "mensagem": base_details["mensagem"],
            "data_envio": base_details["data_envio"],
            "caminho_arquivo": base_details["caminho_arquivo"],
            "formato_arquivo": base_details["formato_arquivo"]
        }

class PhotoMessage(MediaMessage):
    """Mensagem com foto."""
    def __init__(self, message: str, file_path: str, file_format: str):
        super().__init__(message, file_path, file_format)

    def get_details(self) -> dict:
        # Polimorfismo: Adiciona o tipo específico
        details = super().get_details()
        details["tipo"] = "Foto"
        return details

    def send(self, channel: 'ChannelBase', recipient: str):
        # Polimorfismo: Implementação específica de envio de foto
        channel.send_photo(self, recipient)

class VideoMessage(MediaMessage):
    """Mensagem com vídeo, incluindo duração."""
    def __init__(self, message: str, file_path: str, file_format: str, duration: int):
        super().__init__(message, file_path, file_format)
        self._duration = duration # Encapsulamento: Atributo específico

    @property
    def duration(self) -> int:
        return self._duration

    def get_details(self) -> dict:
        # Polimorfismo: Adiciona o tipo e a duração
        details = super().get_details()
        details["tipo"] = "Vídeo"
        details["duração_segundos"] = self._duration
        return details

    def send(self, channel: 'ChannelBase', recipient: str):
        # Polimorfismo: Implementação específica de envio de vídeo
        channel.send_video(self, recipient)

class FileMessage(MediaMessage):
    """Mensagem com arquivo genérico."""
    def __init__(self, message: str, file_path: str, file_format: str):
        super().__init__(message, file_path, file_format)

    def get_details(self) -> dict:
        # Polimorfismo: Adiciona o tipo específico
        details = super().get_details()
        details["tipo"] = "Arquivo"
        return details

    def send(self, channel: 'ChannelBase', recipient: str):
        # Polimorfismo: Implementação específica de envio de arquivo
        channel.send_file(self, recipient)

# ----------------------------------------------------------------------
# Classes de Canais
# ----------------------------------------------------------------------

class ChannelBase(ABC):
    """
    Classe base abstrata para todos os canais de comunicação.
    Define a interface de envio (Polimorfismo).
    """
    def __init__(self, name: str, address_type: str):
        self._name = name
        self._address_type = address_type # Tipo de endereço: 'telefone' ou 'usuario'

    @property
    def name(self) -> str:
        return self._name

    @property
    def address_type(self) -> str:
        return self._address_type

    def _validate_recipient(self, recipient: str):
        """Método interno para validação básica do destinatário (Encapsulamento)."""
        if not recipient:
            raise ValueError("O destinatário não pode ser vazio.")
        print(f"Validando destinatário '{recipient}' para canal {self._name} ({self._address_type})...")

    # Polimorfismo: Métodos abstratos para cada tipo de mensagem
    @abstractmethod
    def send_text(self, message: TextMessage, recipient: str):
        pass

    @abstractmethod
    def send_photo(self, message: PhotoMessage, recipient: str):
        pass

    @abstractmethod
    def send_video(self, message: VideoMessage, recipient: str):
        pass

    @abstractmethod
    def send_file(self, message: FileMessage, recipient: str):
        pass

class WhatsAppChannel(ChannelBase):
    """Canal WhatsApp (Endereçamento por Telefone)."""
    def __init__(self):
        # Herança: Inicializa com nome e tipo de endereço
        super().__init__("WhatsApp", "telefone")

    def send_text(self, message: TextMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando TEXTO para {recipient} (Telefone): {message.message}")

    def send_photo(self, message: PhotoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando FOTO para {recipient} (Telefone): {message.file_path} ({message.file_format}) - {message.message}")

    def send_video(self, message: VideoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando VÍDEO para {recipient} (Telefone): {message.file_path} ({message.file_format}, {message.duration}s) - {message.message}")

    def send_file(self, message: FileMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando ARQUIVO para {recipient} (Telefone): {message.file_path} ({message.file_format}) - {message.message}")

class TelegramChannel(ChannelBase):
    """Canal Telegram (Endereçamento por Telefone ou Usuário)."""
    def __init__(self, address_type: str):
        # Encapsulamento: Garante que o tipo de endereço é válido
        if address_type not in ["telefone", "usuario"]:
            raise ValueError("Tipo de endereço inválido para Telegram. Use 'telefone' ou 'usuario'.")
        super().__init__("Telegram", address_type)

    def send_text(self, message: TextMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando TEXTO para {recipient} ({self.address_type}): {message.message}")

    def send_photo(self, message: PhotoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando FOTO para {recipient} ({self.address_type}): {message.file_path} ({message.file_format}) - {message.message}")

    def send_video(self, message: VideoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando VÍDEO para {recipient} ({self.address_type}): {message.file_path} ({message.file_format}, {message.duration}s) - {message.message}")

    def send_file(self, message: FileMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando ARQUIVO para {recipient} ({self.address_type}): {message.file_path} ({message.file_format}) - {message.message}")

class FacebookChannel(ChannelBase):
    """Canal Facebook (Endereçamento por Usuário)."""
    def __init__(self):
        super().__init__("Facebook", "usuario")

    def send_text(self, message: TextMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando TEXTO para {recipient} (Usuário): {message.message}")

    def send_photo(self, message: PhotoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando FOTO para {recipient} (Usuário): {message.file_path} ({message.file_format}) - {message.message}")

    def send_video(self, message: VideoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando VÍDEO para {recipient} (Usuário): {message.file_path} ({message.file_format}, {message.duration}s) - {message.message}")

    def send_file(self, message: FileMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando ARQUIVO para {recipient} (Usuário): {message.file_path} ({message.file_format}) - {message.message}")

class InstagramChannel(ChannelBase):
    """Canal Instagram (Endereçamento por Usuário)."""
    def __init__(self):
        super().__init__("Instagram", "usuario")

    def send_text(self, message: TextMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando TEXTO para {recipient} (Usuário): {message.message}")

    def send_photo(self, message: PhotoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando FOTO para {recipient} (Usuário): {message.file_path} ({message.file_format}) - {message.message}")

    def send_video(self, message: VideoMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando VÍDEO para {recipient} (Usuário): {message.file_path} ({message.file_format}, {message.duration}s) - {message.message}")

    def send_file(self, message: FileMessage, recipient: str):
        self._validate_recipient(recipient)
        print(f"[{self.name}] Enviando ARQUIVO para {recipient} (Usuário): {message.file_path} ({message.file_format}) - {message.message}")

# ----------------------------------------------------------------------
# Classe de Serviço (Facade)
# ----------------------------------------------------------------------

class MessageService:
    """
    Classe de serviço que atua como uma fachada para o sistema de envio.
    Gerencia a lógica de envio e a seleção do canal.
    """
    def __init__(self):
        # Inicializa os canais disponíveis
        self.whatsapp = WhatsAppChannel()
        self.telegram_phone = TelegramChannel("telefone")
        self.telegram_user = TelegramChannel("usuario")
        self.facebook = FacebookChannel()
        self.instagram = InstagramChannel()

    def send_message(self, channel_name: str, recipient: str, message: MessageBase):
        """
        Método principal para enviar qualquer tipo de mensagem para um canal.
        """
        channel_name = channel_name.lower()

        # Seleção do canal e tipo de endereço
        if channel_name == "whatsapp":
            channel = self.whatsapp
        elif channel_name == "telegram":
            # Lógica para escolher entre telefone ou usuário no Telegram
            # Assumimos que se o destinatário for um número, é telefone, senão é usuário.
            # Em um sistema real, essa lógica seria mais robusta.
            if recipient.replace('+', '').isdigit():
                channel = self.telegram_phone
            else:
                channel = self.telegram_user
        elif channel_name == "facebook":
            channel = self.facebook
        elif channel_name == "instagram":
            channel = self.instagram
        else:
            raise ValueError(f"Canal '{channel_name}' não suportado.")

        # Verifica se o tipo de endereço do canal é compatível com o destinatário
        if channel.address_type == "telefone" and not recipient.replace('+', '').isdigit():
            print(f"AVISO: O canal {channel.name} espera um número de telefone, mas recebeu '{recipient}'. Tentando enviar mesmo assim.")
        elif channel.address_type == "usuario" and recipient.replace('+', '').isdigit():
            print(f"AVISO: O canal {channel.name} espera um nome de usuário, mas recebeu '{recipient}'. Tentando enviar mesmo assim.")

        # Polimorfismo: O objeto 'message' sabe como se enviar para o 'channel'
        message.send(channel, recipient)
        print(f"Detalhes da Mensagem Enviada: {message.get_details()}")

# ----------------------------------------------------------------------
# Exemplo de Uso
# ----------------------------------------------------------------------

def run_example():
    service = MessageService()

    # 1. Mensagem de Texto
    text_msg = TextMessage("Olá! Esta é uma mensagem de teste.")

    # 2. Mensagem de Foto
    photo_msg = PhotoMessage(
        message="Selfie do dia",
        file_path="/caminho/para/foto.jpg",
        file_format="JPEG"
    )

    # 3. Mensagem de Vídeo
    video_msg = VideoMessage(
        message="Vídeo da apresentação",
        file_path="/caminho/para/video.mp4",
        file_format="MP4",
        duration=120
    )

    # 4. Mensagem de Arquivo
    file_msg = FileMessage(
        message="Relatório Mensal",
        file_path="/caminho/para/relatorio.pdf",
        file_format="PDF"
    )

    print("="*50)
    print("TESTE DE ENVIO DE MENSAGENS")
    print("="*50)

    # Teste 1: WhatsApp (Telefone) - Texto
    print("\n--- Teste 1: WhatsApp (Texto) ---")
    service.send_message("whatsapp", "+5511987654321", text_msg)

    # Teste 2: Facebook (Usuário) - Foto
    print("\n--- Teste 2: Facebook (Foto) ---")
    service.send_message("facebook", "usuario_facebook_id", photo_msg)

    # Teste 3: Telegram (Telefone) - Vídeo
    print("\n--- Teste 3: Telegram (Vídeo - Telefone) ---")
    service.send_message("telegram", "+1234567890", video_msg)

    # Teste 4: Instagram (Usuário) - Arquivo (Nota: Arquivos genéricos podem não ser suportados no Instagram real)
    print("\n--- Teste 4: Instagram (Arquivo) ---")
    service.send_message("instagram", "@meu_perfil", file_msg)

    # Teste 5: Telegram (Usuário) - Texto
    print("\n--- Teste 5: Telegram (Texto - Usuário) ---")
    service.send_message("telegram", "meu_username_telegram", text_msg)

    # Teste 6: WhatsApp (Telefone) - Vídeo
    print("\n--- Teste 6: WhatsApp (Vídeo) ---")
    service.send_message("whatsapp", "+5511987654321", video_msg)

if __name__ == '__main__':
    run_example()
