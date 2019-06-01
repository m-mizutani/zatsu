package main

import (
	"crypto/sha256"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
)

func getSha256(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()

	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", h.Sum(nil)), nil
}

func rename(path string) error {
	hash, err := getSha256(path)
	if err != nil {
		return err
	}

	dirName := filepath.Dir(path)
	ext := filepath.Ext(path)
	newPath := filepath.Join(dirName, hash+ext)

	log.Printf("rename: %s to %s\n", path, newPath)
	if err := os.Rename(path, newPath); err != nil {
		return err
	}

	return nil
}

func renameAll(pathList []string) error {
	for _, basePath := range pathList {
		log.Println("basePath:", basePath)
		stat, err := os.Stat(basePath)
		if err != nil {
			return err
		}

		if stat.IsDir() {
			err := filepath.Walk(basePath, func(path string, info os.FileInfo, err error) error {
				if err != nil {
					return err
				}

				if !info.IsDir() {
					if err := rename(path); err != nil {
						return err
					}
				} else {
					log.Printf("%s is dir, skip", path)
				}
				return nil
			})

			if err != nil {
				return err
			}
		} else {
			if err := rename(basePath); err != nil {
				return err
			}
		}
	}

	return nil
}

func main() {
	if err := renameAll(os.Args[1:]); err != nil {
		log.Fatal(err)
	}
}
