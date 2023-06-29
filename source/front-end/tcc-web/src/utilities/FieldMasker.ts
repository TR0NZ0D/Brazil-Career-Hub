class FieldMasker {
  static maskCpf(v: string) {

    if (v === null || v === "")
      return "";

    v = v.replace(/\D/g, "")
    if (v.length <= 11) {
      v = v.replace(/(\d{3})(\d)/, "$1.$2")
      v = v.replace(/(\d{3})(\d)/, "$1.$2")
      v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2")
    }

    else
      throw new Error("Invalid CPF length")

    return v
  }

  static maskCnpj(v: string) {
    v = v.replace(/\D/g, "")

    v = v.replace(/^(\d{2})(\d)/, "$1.$2")
    v = v.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    v = v.replace(/\.(\d{3})(\d)/, ".$1/$2")
    v = v.replace(/(\d{4})(\d)/, "$1-$2")
  }
}

export default FieldMasker;
