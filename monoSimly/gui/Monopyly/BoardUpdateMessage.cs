//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

// Generated from: BoardUpdateMessage.proto
namespace Messaging
{
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"BoardUpdateMessage")]
  public partial class BoardUpdateMessage : global::ProtoBuf.IExtensible
  {
    public BoardUpdateMessage() {}
    
    private readonly global::System.Collections.Generic.List<Messaging.BoardUpdateMessage.SquareInfo> _square_infos = new global::System.Collections.Generic.List<Messaging.BoardUpdateMessage.SquareInfo>();
    [global::ProtoBuf.ProtoMember(1, Name=@"square_infos", DataFormat = global::ProtoBuf.DataFormat.Default)]
    public global::System.Collections.Generic.List<Messaging.BoardUpdateMessage.SquareInfo> square_infos
    {
      get { return _square_infos; }
    }
  
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"SquareInfo")]
  public partial class SquareInfo : global::ProtoBuf.IExtensible
  {
    public SquareInfo() {}
    
    private int _square_number = default(int);
    [global::ProtoBuf.ProtoMember(1, IsRequired = false, Name=@"square_number", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    [global::System.ComponentModel.DefaultValue(default(int))]
    public int square_number
    {
      get { return _square_number; }
      set { _square_number = value; }
    }
    private int _owner_player_number = default(int);
    [global::ProtoBuf.ProtoMember(2, IsRequired = false, Name=@"owner_player_number", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    [global::System.ComponentModel.DefaultValue(default(int))]
    public int owner_player_number
    {
      get { return _owner_player_number; }
      set { _owner_player_number = value; }
    }
    private bool _is_mortgaged = default(bool);
    [global::ProtoBuf.ProtoMember(3, IsRequired = false, Name=@"is_mortgaged", DataFormat = global::ProtoBuf.DataFormat.Default)]
    [global::System.ComponentModel.DefaultValue(default(bool))]
    public bool is_mortgaged
    {
      get { return _is_mortgaged; }
      set { _is_mortgaged = value; }
    }
    private int _number_of_houses = default(int);
    [global::ProtoBuf.ProtoMember(4, IsRequired = false, Name=@"number_of_houses", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    [global::System.ComponentModel.DefaultValue(default(int))]
    public int number_of_houses
    {
      get { return _number_of_houses; }
      set { _number_of_houses = value; }
    }
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
}