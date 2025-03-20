{
  source ? import ./npins,
  system ? builtins.currentSystem,
  pkgs ? import source.nixpkgs {
    overlays = [ ];
    config = { };
    inherit system;
  },
  poetry2nix ? import source.poetry2nix { inherit pkgs; },
}:

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  preferWheels = true;
}
