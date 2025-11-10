public abstract class MessageBase
{
    protected MessageBase(string message){
        Message = message;
        SentAt = DateTime.Now;
    }

    public string Message { get; }
    public DateTime SentAt { get;}
}