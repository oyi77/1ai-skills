"""
Team Onboarding Module - Configure notification preferences for team members.

This module manages notification preferences for BerkahKarya team members:
- Paijo (Owner/Founder)
- Veris (Ads Master)
- Sony (Ops Manager)
- Nuno (Trading Master)

Supports multiple notification channels: telegram, email, whatsapp
Includes quiet hours configuration and language preferences.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class QuietHours:
    """Configuration for quiet hours when notifications should be suppressed."""

    enabled: bool = True
    start_time: str = "22:00"  # HH:MM format
    end_time: str = "08:00"  # HH:MM format
    timezone: str = "Asia/Jakarta"


@dataclass
class NotificationChannel:
    """Configuration for a single notification channel."""

    name: str  # telegram, email, whatsapp
    enabled: bool = True
    priority: int = 1  # 1=high, 2=medium, 3=low


@dataclass
class TeamMember:
    """Represents a team member with their notification preferences."""

    name: str
    role: str
    email: str
    telegram_id: Optional[str] = None
    whatsapp_number: Optional[str] = None
    language: str = "id"  # id=Indonesian, en=English
    channels: List[NotificationChannel] = field(default_factory=list)
    quiet_hours: QuietHours = field(default_factory=QuietHours)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "telegram_id": self.telegram_id,
            "whatsapp_number": self.whatsapp_number,
            "language": self.language,
            "channels": [
                {"name": ch.name, "enabled": ch.enabled, "priority": ch.priority}
                for ch in self.channels
            ],
            "quiet_hours": {
                "enabled": self.quiet_hours.enabled,
                "start_time": self.quiet_hours.start_time,
                "end_time": self.quiet_hours.end_time,
                "timezone": self.quiet_hours.timezone,
            },
        }


class TeamOnboarding:
    """Manages team member onboarding and notification preferences."""

    def __init__(self, config_file: str = None):
        """
        Initialize TeamOnboarding.

        Args:
            config_file: Path to JSON config file. Defaults to team_preferences.json
        """
        if config_file is None:
            config_file = os.path.join(
                os.path.dirname(__file__), "team_preferences.json"
            )
        self.config_file = config_file
        self.team_members: Dict[str, TeamMember] = {}
        self._initialize_team()

    def _initialize_team(self):
        """Initialize team members with default preferences."""
        # Paijo - Owner/Founder
        paijo = TeamMember(
            name="Paijo",
            role="Owner/Founder",
            email="paijo@berkahkarya.com",
            telegram_id="paijo_tg",
            whatsapp_number="+62812345678",
            language="id",
            channels=[
                NotificationChannel("telegram", enabled=True, priority=1),
                NotificationChannel("email", enabled=True, priority=2),
                NotificationChannel("whatsapp", enabled=True, priority=3),
            ],
            quiet_hours=QuietHours(
                enabled=True,
                start_time="23:00",
                end_time="07:00",
                timezone="Asia/Jakarta",
            ),
        )

        # Veris - Ads Master
        veris = TeamMember(
            name="Veris",
            role="Ads & Marketing Master",
            email="veris@berkahkarya.com",
            telegram_id="veris_tg",
            whatsapp_number="+62812345679",
            language="id",
            channels=[
                NotificationChannel("telegram", enabled=True, priority=1),
                NotificationChannel("email", enabled=True, priority=2),
                NotificationChannel("whatsapp", enabled=False, priority=3),
            ],
            quiet_hours=QuietHours(
                enabled=True,
                start_time="22:00",
                end_time="08:00",
                timezone="Asia/Jakarta",
            ),
        )

        # Sony - Ops Manager
        sony = TeamMember(
            name="Sony",
            role="Operational Manager",
            email="sony@berkahkarya.com",
            telegram_id="sony_tg",
            whatsapp_number="+62812345680",
            language="id",
            channels=[
                NotificationChannel("telegram", enabled=True, priority=1),
                NotificationChannel("email", enabled=True, priority=2),
                NotificationChannel("whatsapp", enabled=True, priority=2),
            ],
            quiet_hours=QuietHours(
                enabled=True,
                start_time="21:00",
                end_time="09:00",
                timezone="Asia/Jakarta",
            ),
        )

        # Nuno - Trading Master
        nuno = TeamMember(
            name="Nuno",
            role="Trading Master",
            email="nuno@berkahkarya.com",
            telegram_id="nuno_tg",
            whatsapp_number="+62812345681",
            language="en",
            channels=[
                NotificationChannel("telegram", enabled=True, priority=1),
                NotificationChannel("email", enabled=True, priority=3),
                NotificationChannel("whatsapp", enabled=True, priority=2),
            ],
            quiet_hours=QuietHours(
                enabled=False,  # Trading requires 24/7 monitoring
                start_time="00:00",
                end_time="00:00",
                timezone="Asia/Jakarta",
            ),
        )

        self.team_members = {
            "paijo": paijo,
            "veris": veris,
            "sony": sony,
            "nuno": nuno,
        }

    def get_member(self, name: str) -> Optional[TeamMember]:
        """Get a team member by name (case-insensitive)."""
        return self.team_members.get(name.lower())

    def update_member_preferences(
        self,
        name: str,
        language: Optional[str] = None,
        channels: Optional[List[Dict]] = None,
        quiet_hours: Optional[Dict] = None,
    ) -> bool:
        """
        Update preferences for a team member.

        Args:
            name: Team member name
            language: Language preference (id/en)
            channels: List of channel configs
            quiet_hours: Quiet hours configuration

        Returns:
            True if update successful, False otherwise
        """
        member = self.get_member(name)
        if not member:
            return False

        if language:
            member.language = language

        if channels:
            member.channels = [
                NotificationChannel(
                    name=ch.get("name"),
                    enabled=ch.get("enabled", True),
                    priority=ch.get("priority", 1),
                )
                for ch in channels
            ]

        if quiet_hours:
            member.quiet_hours = QuietHours(
                enabled=quiet_hours.get("enabled", True),
                start_time=quiet_hours.get("start_time", "22:00"),
                end_time=quiet_hours.get("end_time", "08:00"),
                timezone=quiet_hours.get("timezone", "Asia/Jakarta"),
            )

        return True

    def get_active_channels(self, name: str) -> List[str]:
        """Get list of active notification channels for a member."""
        member = self.get_member(name)
        if not member:
            return []
        return [ch.name for ch in member.channels if ch.enabled]

    def is_in_quiet_hours(self, name: str, current_time: datetime = None) -> bool:
        """
        Check if current time is within quiet hours for a member.

        Args:
            name: Team member name
            current_time: Time to check (defaults to now)

        Returns:
            True if in quiet hours, False otherwise
        """
        member = self.get_member(name)
        if not member or not member.quiet_hours.enabled:
            return False

        if current_time is None:
            current_time = datetime.now()

        current_hour = current_time.strftime("%H:%M")
        start = member.quiet_hours.start_time
        end = member.quiet_hours.end_time

        # Handle case where quiet hours span midnight
        if start > end:  # e.g., 22:00 to 08:00
            return current_hour >= start or current_hour < end
        else:  # e.g., 14:00 to 16:00
            return start <= current_hour < end

    def save_preferences(self) -> bool:
        """Save all team preferences to JSON file."""
        try:
            preferences = {
                "timestamp": datetime.now().isoformat(),
                "team_members": {
                    name: member.to_dict() for name, member in self.team_members.items()
                },
            }

            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, "w") as f:
                json.dump(preferences, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False

    def load_preferences(self) -> bool:
        """Load team preferences from JSON file."""
        try:
            if not os.path.exists(self.config_file):
                return False

            with open(self.config_file, "r") as f:
                data = json.load(f)

            # Reconstruct team members from loaded data
            for name, member_data in data.get("team_members", {}).items():
                channels = [
                    NotificationChannel(
                        name=ch["name"],
                        enabled=ch.get("enabled", True),
                        priority=ch.get("priority", 1),
                    )
                    for ch in member_data.get("channels", [])
                ]

                qh_data = member_data.get("quiet_hours", {})
                quiet_hours = QuietHours(
                    enabled=qh_data.get("enabled", True),
                    start_time=qh_data.get("start_time", "22:00"),
                    end_time=qh_data.get("end_time", "08:00"),
                    timezone=qh_data.get("timezone", "Asia/Jakarta"),
                )

                member = TeamMember(
                    name=member_data["name"],
                    role=member_data["role"],
                    email=member_data["email"],
                    telegram_id=member_data.get("telegram_id"),
                    whatsapp_number=member_data.get("whatsapp_number"),
                    language=member_data.get("language", "id"),
                    channels=channels,
                    quiet_hours=quiet_hours,
                )

                self.team_members[name] = member

            return True
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return False

    def get_summary(self) -> Dict:
        """Get summary of all team members and their preferences."""
        return {
            "total_members": len(self.team_members),
            "members": {
                name: {
                    "name": member.name,
                    "role": member.role,
                    "email": member.email,
                    "language": member.language,
                    "active_channels": self.get_active_channels(name),
                    "quiet_hours_enabled": member.quiet_hours.enabled,
                    "quiet_hours": f"{member.quiet_hours.start_time} - {member.quiet_hours.end_time}",
                }
                for name, member in self.team_members.items()
            },
        }


def main():
    """Example usage of TeamOnboarding."""
    # Initialize team onboarding
    onboarding = TeamOnboarding()

    # Display team summary
    print("=" * 60)
    print("BERKAHKARYA TEAM ONBOARDING")
    print("=" * 60)

    summary = onboarding.get_summary()
    print(f"\nTotal Team Members: {summary['total_members']}\n")

    for name, info in summary["members"].items():
        print(f"Name: {info['name']}")
        print(f"Role: {info['role']}")
        print(f"Email: {info['email']}")
        print(f"Language: {info['language']}")
        print(f"Active Channels: {', '.join(info['active_channels'])}")
        print(
            f"Quiet Hours: {info['quiet_hours']} (Enabled: {info['quiet_hours_enabled']})"
        )
        print("-" * 60)

    # Save preferences to JSON
    if onboarding.save_preferences():
        print(f"\n✓ Preferences saved to: {onboarding.config_file}")
    else:
        print(f"\n✗ Failed to save preferences")

    # Example: Check if Paijo is in quiet hours
    print(f"\nPaijo in quiet hours now: {onboarding.is_in_quiet_hours('paijo')}")

    # Example: Get active channels for Nuno
    print(f"Nuno's active channels: {onboarding.get_active_channels('nuno')}")


if __name__ == "__main__":
    main()
