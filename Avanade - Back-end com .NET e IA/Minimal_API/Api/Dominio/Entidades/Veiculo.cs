using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalAPI.Entidades;

public class Veiculo
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } = default!;
    
    [Required]
    [StringLength(150)]
    public string Nome { get; set; } = default!;

    [StringLength(100)]
    public String Marca { get; set; } = default!;

    public int Ano { get; set; } = default!;
}