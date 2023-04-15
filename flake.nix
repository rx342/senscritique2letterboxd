{
  description = "senscritique2letterboxd flake";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShell = pkgs.mkShell {
          nativeBuildInputs = pkgs.lib.attrsets.attrVals (
            pkgs.lib.lists.init (
              pkgs.lib.strings.splitString "\n" (builtins.readFile ./requirements.txt)
            )
          ) pkgs.python310Packages;
        };
      }
    );
}
