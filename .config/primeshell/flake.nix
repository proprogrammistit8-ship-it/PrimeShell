{
  description = "NixOS Flakes Module System For PrimeShell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    fabric.url = "github:Fabric-Development/fabric";
  };

  outputs = { self, nixpkgs, fabric, ... } @ inputs: 
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "primeshell-env";

      buildInputs = with pkgs; [
        librsvg
        gobject-introspection
        # Добавь сюда остальные пакеты для разработки
      ];

      # Подтягиваем окружение из самого Fabric
      inputsFrom = [
        fabric.devShells.${system}.default
      ];

      shellHook = ''
        export GI_TYPELIB_PATH=${pkgs.librsvg}/lib/girepository-1.0:$GI_TYPELIB_PATH
        echo "PrimeShell development environment loaded!"
      '';
    };
  };
}

