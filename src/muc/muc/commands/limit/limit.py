import logging
import shutil
from pathlib import Path

import ffmpeg
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError

DEFAULT_LIMIT_BITRATE = 1411000
DEFAULT_LIMIT_BIT_DEPTH = 16
DEFAULT_LIMIT_SAMPLING_RATE = 44100


class CommandLimit:
    def __init__(self: "CommandLimit", cfg: Configuration) -> None:
        self.bitrate: int = cfg.get_configuration_item_or_default(
            "limit_flac_bitrate",
            DEFAULT_LIMIT_BITRATE,
        )
        self.bit_depth: int = cfg.get_configuration_item_or_default(
            "limit_flac_bit_depth",
            DEFAULT_LIMIT_BIT_DEPTH,
        )
        self.sampling_rate: int = cfg.get_configuration_item_or_default(
            "limit_flac_sampling_rate",
            DEFAULT_LIMIT_SAMPLING_RATE,
        )
        try:
            self.source_dir = Path(str(cfg.get_configuration_item("limit_path_source")))
        except ConfigurationKeyNotFoundError as e:
            raise ConfigurationKeyNotFoundError from e
        try:
            self.output_dir = Path(str(cfg.get_configuration_item("limit_path_output")))
        except ConfigurationKeyNotFoundError as e:
            raise ConfigurationKeyNotFoundError from e

    def execute(self: "CommandLimit") -> None:
        for file_path in self.source_dir.rglob("*.flac"):
            if not file_path.is_relative_to(self.output_dir):
                self.transcode_flac(file_path)

    def transcode_flac(self: "CommandLimit", file_path: Path) -> None:
        """
        Processes a FLAC file by either transcoding or copying it to the output directory.

        Args:
            file_path (Path): The path to the FLAC file.
        """
        try:
            # Get the audio stream information
            probe = ffmpeg.probe(str(file_path), loglevel="quiet")
            audio_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "audio"
                ),
                None,
            )

            relative_path = file_path.relative_to(self.source_dir)
            output_path = self.output_dir / relative_path

            # Create the output directory structure if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if audio_stream:
                bitrate = int(audio_stream.get("bit_rate", 0))
                sampling_rate = int(audio_stream.get("sample_rate", 0))
                bit_depth = int(audio_stream.get("bits_per_sample", 0))

                if (
                    bitrate > self.bitrate
                    or sampling_rate > self.sampling_rate
                    or bit_depth > self.bit_depth
                ):
                    # Transcode the FLAC file with the specified parameters
                    stream = ffmpeg.input(str(file_path))
                    stream = ffmpeg.output(
                        stream,
                        str(output_path),
                        audio_bitrate=f"{self.bitrate}",
                        ar=f"{self.sampling_rate}",
                        sample_fmt=f"s{self.bit_depth}",
                        loglevel="quiet",
                    )
                    ffmpeg.run(stream, overwrite_output=True)

                    logging.info("Transcoded: %s  -> %s", file_path, output_path)
                else:
                    # Copy the FLAC file to the output directory
                    shutil.copy2(file_path, output_path)
                    logging.info("Copied: %s  -> %s", file_path, output_path)
                    print(f"Copied: {file_path} -> {output_path}")
            else:
                logging.warning("Skipped (no audio stream found): %s", file_path)
        except ffmpeg.Error as e:
            logging.exception("Error processing %s: %s", file_path, e.stderr)
